function initApp() {
  // Install built-in polyfills to patch browser incompatibilities.
  shaka.polyfill.installAll();

  // Check to see if the browser supports the basic APIs Shaka needs.
  if (shaka.Player.isBrowserSupported()) {
    // Everything looks good!

  } else {
    // This browser does not have the minimum set of APIs we need.
    console.error('Browser not supported!');
  }
}

// Listen to the custom shaka-ui-loaded event, to wait until the UI is loaded.
document.addEventListener('shaka-ui-loaded', () => {
  const processor = new Processor();
  processor.initPlayer();
});
// Listen to the custom shaka-ui-load-failed event, in case Shaka Player fails
// to load (e.g. due to lack of browser support).
document.addEventListener('shaka-ui-load-failed', initFailed);

function initFailed(errorEvent) {
  // Handle the failure to load; errorEvent.detail.reasonCode has a
  // shaka.ui.FailReasonCode describing why.
  console.error('Unable to load the UI library!');
}

const TIMES_SIZE = 50;
const CLOCK_SIZE = 50;
const COLORS = [
  /* Red */
'#f44336',

/* Pink */
'#e91e63',

/* Purple */
'#9c27b0',

/* Deep Purple */
'#673ab7',

/* Indigo */
'#3f51b5',

/* Blue */
'#2196f3',

/* Light Blue */
'#03a9f4',

/* Cyan */
'#00bcd4',

/* Teal */
'#009688',

/* Green */
'#4caf50',

/* Light Green */
'#8bc34a',

/* Lime */
'#cddc39',

/* Yellow */
'#ffeb3b',

/* Amber */
'#ffc107',

/* Orange */
'#ff9800',

/* Deep Orange */
'#ff5722',

/* Brown */
'#795548',

/* Grey */
'#9e9e9e',

/* Blue Grey */
'#607d8b'
]

class Processor {

  constructor() {
    this.start = null;
    this.currentTime = null;
  }

  /*
    Note: 1st POC used multiple canvases. I think this will be faster
  */
  render() {
    const videoTime = this.video.currentTime;
    if(videoTime != this.currentTime) {
      this.currentTime = videoTime;

      const context = this.canvas.getContext('2d');
      context.clearRect(0, 0, this.canvas.width, this.canvas.height);
      this.layers.forEach((_, idx) => {
        if(this.displays[idx]) {
          const imgHeight = this.video.videoHeight/this.layers.length;
          context.drawImage(this.video, 
              0, idx*imgHeight, this.video.videoWidth, imgHeight, 
              0, 0, canvas.width, canvas.height);
          context.fillStyle = 'white';
          context.fillText(videoTime, 50, 50); 
        }
      });

      if(this.metrics.getFrameCount() % 10 == 0) {
        this.metricContainer.textContent = "requestAnimationFrame/s: " + this.metrics.fps();
      }
    }
  }

  // function step(timestamp) {
  //   if (start === undefined)
  //     start = timestamp;
  //   const elapsed = timestamp - start;
  
  //   // `Math.min()` is used here to make sure that the element stops at exactly 200px.
  //   element.style.transform = 'translateX(' + Math.min(0.1 * elapsed, 200) + 'px)';
  
  //   if (elapsed < 2000) { // Stop the animation after 2 seconds
  //     window.requestAnimationFrame(step);
  //   }
  // }

  draw(timestamp) {
    if (this.start == null) {
      this.start = timestamp;
    }
    if (this.video.paused || this.video.ended) {
      return;
    }

    this.render();

    this.metrics.tick();
    window.requestAnimationFrame(this.draw.bind(this));
  }

   onPlayerErrorEvent(errorEvent) {
    // Extract the shaka.util.Error object from the event.
    onPlayerError(event.detail);
  }
  
  onPlayerError(error) {
    // Handle player error
    console.error('Error code', error.code, 'object', error);
  }
  
  onUIErrorEvent(errorEvent) {
    // Extract the shaka.util.Error object from the event.
    onPlayerError(event.detail);
  }

  async initPlayer() {
    const urlParams = new URLSearchParams(window.location.search);
    if(!urlParams.has('url')) {
      return;
    }

    const url = urlParams.get('url');

    // Create a Player instance.
    this.video = document.getElementById('video');
    const ui = this.video['ui'];

  //     /** @private */
  // configureUI_() {
  //   const video = /** @type {!HTMLVideoElement} */ (this.video_);
  //   const ui = video['ui'];

  //   const uiConfig = ui.getConfiguration();
  //   // Remove any trick play configurations from a previous config.
  //   uiConfig.addSeekBar = true;
  //   uiConfig.controlPanelElements =
  //       uiConfig.controlPanelElements.filter((element) => {
  //         return element != 'rewind' && element != 'fast_forward';
  //       });
  //   if (this.trickPlayControlsEnabled_) {
  //     // Trick mode controls don't have a seek bar.
  //     uiConfig.addSeekBar = false;
  //     // Replace the position the play_pause button was at with a full suite of
  //     // trick play controls, including rewind and fast-forward.
  //     const index = uiConfig.controlPanelElements.indexOf('play_pause');
  //     uiConfig.controlPanelElements.splice(
  //         index, 1, 'rewind', 'play_pause', 'fast_forward');
  //   }
  //   if (!uiConfig.controlPanelElements.includes('close')) {
  //     uiConfig.controlPanelElements.push('close');
  //   }
  //   ui.configure(uiConfig);
  // }


    const controls = ui.getControls();
    const player = controls.getPlayer();
    const config = {
      'addSeekBar': false,
      'controlPanelElements': ['rewind', 'play_pause', 'fast_forward', 'spacer', 'time_and_duration', 'overflow_menu'],
      'overflowMenuButtons' : ['quality', 'loop', 'playback_rate']
    }
    ui.configure(config);
    console.log(player.getStats());

    this.canvas = document.getElementById('canvas');
    this.metricContainer = document.getElementById('metric-container');
    this.metrics = new Metrics(TIMES_SIZE);
    this.clockMetrics = new Metrics(CLOCK_SIZE);
    // const player = new shaka.Player(video);

    // Attach player and ui to the window to make it easy to access in the JS console.
    window.player = player;
    window.ui = ui;

    // Listen for error events.
    player.addEventListener('error', this.onPlayerErrorEvent.bind(this));
    controls.addEventListener('error', this.onUIErrorEvent.bind(this));


    // Try to load a manifest.
    // This is an asynchronous process.
    try {
      await player.load(url);
      // This runs if the asynchronous load is successful.
      console.log('The video has now been loaded!');

      const controlContainer = document.getElementById('control-container');
      this.layers = [];
      const tile_manifest = url.replace('output.webm', 'tile_manifest.json').replace('output.mpd', 'tile_manifest.json');
      fetch(tile_manifest, {
        //credentials: 'include'
      }).then(response => response.json()).then(data => {
        this.displays = []

        Object.entries(data).forEach((entry, idx) => {
            this.displays.push(true);
            const name = entry[0];
            const {x,y /* ,width, height */} = entry[1];
            const controlDiv = document.createElement('div');
  
            const checkBox = document.createElement('input');
            checkBox.id = name + '_checkBox';
            checkBox.type = 'checkbox';
            checkBox.checked = name != 'camera_line_segmentation';
            this.displays[idx] = checkBox.checked;
            const label = document.createElement('label');
            label.for = name + '_checkBox';
            label.innerHTML = name;
  
            this.layers.push({x,y,name});
  
            checkBox.onchange = () => {
                this.displays[idx] = checkBox.checked;
            }
            controlDiv.appendChild(checkBox);
            controlDiv.appendChild(label);
  
            controlContainer.appendChild(controlDiv);
        });
      });
      this.video.addEventListener( "loadedmetadata", e => {
          console.log('loadedmetadata');
          // this.canvas.width = this.video.width;
          // this.canvas.height = this.video.height/this.layers.length;
      }, false );
      this.video.addEventListener("play", () => {
          console.log('play event');
          
          this.metrics.tick();
          window.requestAnimationFrame(this.draw.bind(this));
        }, false);
    } catch (e) {
      // onError is executed if the asynchronous load fails.
      this.onPlayerError(e);
    }
  }
}

class Metrics {
  constructor(times_size) {
    this.times = []
    for(var i = 0; i < times_size; i++) {
      this.times.push(null);
    }
    this.frameCount = 0;
  }
  tick() {
    this.times[this.frameCount % this.times.length] = (new Date()).getTime();
    this.frameCount++;
  }

  getFrameCount() {
    return this.frameCount;
  }

  fps() {
    const intervals = [];
    this.times.forEach((time, idx, times) => {
      intervals[idx] = times[(idx+1) % this.times.length] - time;
    });
    return Math.floor(1000/intervals[this.frameCount % this.times.length]);
  }
}

document.addEventListener('DOMContentLoaded', initApp);