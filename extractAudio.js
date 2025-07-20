const ffmpeg = require('fluent-ffmpeg');
const ffmpegPath = require('ffmpeg-static');
const path = require('path');

ffmpeg.setFfmpegPath(ffmpegPath);

function extractAudio(videoPath, outputPath) {
  return new Promise((resolve, reject) => {
    ffmpeg(videoPath)
      .output(outputPath)
      .noVideo()
      .audioCodec('pcm_s16le')
      .on('end', () => {
        console.log('✅ Audio extraction complete.');
        resolve(outputPath);
      })
      .on('error', (err) => {
        console.error('❌ Error during audio extraction:', err.message);
        reject(err);
      })
      .run();
  });
}

module.exports = extractAudio;
