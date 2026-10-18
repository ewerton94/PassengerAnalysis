<template>
  <div
    ref="heatmap"
    :style="`width: ${mapWidth}; height: ${mapHeight}`"
  />
</template>

<script>
function loadGoogleMaps (apiKey) {
  if (typeof window === 'undefined') {
    return Promise.reject(new Error('window unavailable'))
  }
  if (window.google?.maps?.visualization) {
    return Promise.resolve(window.google)
  }
  if (window.__gmapsPromise) {
    return window.__gmapsPromise
  }

  window.__gmapsPromise = new Promise((resolve, reject) => {
    const script = document.createElement('script')
    script.src = `https://maps.googleapis.com/maps/api/js?key=${encodeURIComponent(apiKey)}&libraries=visualization`
    script.async = true
    script.onload = () => resolve(window.google)
    script.onerror = reject
    document.head.appendChild(script)
  })

  return window.__gmapsPromise
}

export default {
  name: 'HeatMap',
  props: {
    lat: { type: Number, default: -9.6658 },
    lng: { type: Number, default: -35.735 },
    initialZoom: { type: Number, default: 13 },
    mapType: { type: String, default: 'roadmap' },
    points: { type: Array, required: true },
    width: { type: [String, Number], default: '100%' },
    height: { type: [String, Number], default: '100%' },
    opacity: { type: Number, default: 1 },
    maxIntensity: { type: Number, default: 5 },
    apiKey: { type: String, default: '' }
  },
  computed: {
    mapWidth () {
      return typeof this.width === 'string' ? this.width : `${this.width}px`
    },
    mapHeight () {
      return typeof this.height === 'string' ? this.height : `${this.height}px`
    }
  },
  watch: {
    points: {
      deep: true,
      handler () {
        this.renderMap()
      }
    }
  },
  mounted () {
    this.renderMap()
  },
  methods: {
    async renderMap () {
      const key = (this.apiKey || process.env.GoogleMapsKey || '').replaceAll('"', '').replaceAll("'", '')
      if (!key) {
        return
      }

      const google = await loadGoogleMaps(key)
      const heatmapPoints = (this.points || []).map(
        point => new google.maps.LatLng(point.lat, point.lng)
      )

      this.$mapObject = new google.maps.Map(this.$refs.heatmap, {
        zoom: this.initialZoom,
        center: { lat: this.lat, lng: this.lng },
        mapTypeId: this.mapType
      })

      this.$heatmap = new google.maps.visualization.HeatmapLayer({
        data: heatmapPoints,
        map: this.$mapObject,
        opacity: this.opacity,
        maxIntensity: this.maxIntensity
      })
    }
  }
}
</script>
