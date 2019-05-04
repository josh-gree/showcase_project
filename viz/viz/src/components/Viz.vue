<template>
  <div>
    <h1 v-if="!allReady">Loading...</h1>
    <svg v-else :width="width" :height="height">
      <g>
        <path :d="line"></path>
      </g>
    </svg>
  </div>
</template>

<script>
import { zip, map } from "underscore";
import { normal } from "prob.js";
import * as d3 from "d3";
import { stats } from "science";
export default {
  name: "Viz",
  beforeCreate() {
    this.zip = zip;
    this.map = map;
    this.normal = normal;
    this.d3 = d3;
  },
  created() {
    this.$options.sockets.onopen = () => {
      this.wsReady = true;
    };
    this.$options.sockets.onmessage = evt =>
      (this.params = JSON.parse(evt.data));
  },
  data() {
    return {
      params: {
        means: [],
        vars: []
      },
      nSamples: 3333,
      //   wsReady: false,
      width: 1300,
      height: 600,
      wsReady: false
    };
  },
  computed: {
    allReady() {
      return this.wsReady && this.dataReady;
    },
    dataReady() {
      return this.params.vars.length != 0 && this.params.means.length != 0;
    },
    samples() {
      const mus = this.params.means;
      const sigmas = this.params.vars;
      const n = this.nSamples;
      const zipped = zip(mus, sigmas);
      var samples = [];
      for (const [mu, sigma] of zipped) {
        const sample = this.genSamples(mu, sigma, n);
        samples.push(sample);
      }
      return [].concat.apply([], samples);
    },
    kdedata() {
      const d = stats
        .kde()
        .sample(this.samples)
        .bandwidth(0.05)(this.d3.range(0, 25, 0.1));
      const ys = map(d, d => d[1]);
      const xs = map(d, d => d[0]);
      return { xs, ys };
    },
    line() {
      const x = d3
        .scaleLinear()
        .domain([0, 25])
        .range([0, this.width]);

      const maxys = this.d3.max(this.kdedata.ys);
      const y = d3
        .scaleLinear()
        .domain([this.d3.min(this.kdedata.ys), 1.2 * maxys])
        .range([this.height, 0]);

      return d3
        .line()
        .x(d => x(d[0]))
        .y(d => y(d[1]))(zip(this.kdedata.xs, this.kdedata.ys));
    }
  },
  methods: {
    genSamples(mu, sigma, n) {
      var sample = [];
      const dist = normal(mu, sigma);
      for (var i = 0; i < n; i++) {
        sample.push(dist());
      }
      return sample;
    }
  }
};
</script>

<style scoped>
svg {
  margin: 25px;
}
path {
  fill: none;
  stroke: #76bf8a;
  stroke-width: 3px;
}
</style>