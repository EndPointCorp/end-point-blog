let play_sounds = false;
function sound() { return play_sounds = !play_sounds; }

let play_whistles = false;
function whistle() { return play_whistles = !play_whistles; }

function bufferSound(ctx, url) {
	let p = new Promise(function(resolve, reject) {
		let req = new XMLHttpRequest();
		req.open('GET', url, true);
		req.responseType = 'arraybuffer';
		req.onload = function() {
			ctx.decodeAudioData(req.response, resolve, reject);
		}
		req.send();
	});
	return p;
}

let audioContext = null;
let our_sampled_sound = null;
let our_noise_sound = null;
let our_start_time = 0;

function playSound(the_duration, the_midi, the_time) {
	if (!audioContext) {
		audioContext = new AudioContext();
		our_start_time = audioContext.currentTime;
	}
	if (!our_sampled_sound) {
		const audioSrc = 'pluck.mp3';

		bufferSound(audioContext, audioSrc).then(function (buffer) {
			our_sampled_sound = buffer;
		});
	}

	let bq = audioContext.createBiquadFilter();

	let g = audioContext.createGain();
	g.gain.value = 1;

	let src = audioContext.createBufferSource();
	src.buffer = our_sampled_sound;
	src.playbackRate.value = (2.0**((the_midi-57)/12.0));

	src.connect(bq).connect(g).connect(audioContext.destination);

	src.start(our_start_time + the_time/1000);
}

let noiseDuration = 1;
let midi = 60;

function playNoise(dur, midi, the_time) {
	if (!audioContext) {
		audioContext = new AudioContext();
		our_start_time = audioContext.currentTime;
	}
	const fix_dur = (dur && (dur > 0 && dur < 1000 )) ? dur : 0.1;
	const notchfreq = 440.0 * (2.0**((midi-69)/12.0));
	const bufferSize = audioContext.sampleRate * fix_dur; // set the time of the note
	const buffer = audioContext.createBuffer(1, bufferSize, audioContext.sampleRate); // create an empty buffer
	let data = buffer.getChannelData(0); // get data

	// fill the buffer with noise
	for (let i = 0; i < bufferSize; i++) {
		data[i] = Math.random() * 2 - 1;
	}

	// create a buffer source for our created data
	let noise = audioContext.createBufferSource();
	noise.buffer = buffer;

	let bandpass = audioContext.createBiquadFilter();
	bandpass.type = 'bandpass';
	bandpass.frequency.value = notchfreq;
	bandpass.Q.value = notchfreq * (1.0 - (2 ** 1.0/12.0));
	bandpass.gain.value = 100;

	let g = audioContext.createGain();
	g.gain.value = 12;

	// connect our graph
	noise.connect(bandpass).connect(g).connect(audioContext.destination);
	noise.start(our_start_time + the_time/1000);
}

function noiseplay() {
	playNoise(noiseDuration, midi,      250);
	playNoise(noiseDuration, midi + 7,  400);
	playNoise(noiseDuration, midi + 14, 600);
}

function soundplay() {
	soundDuration = noiseDuration;
	playSound(soundDuration, midi,      250);
	playSound(soundDuration, midi + 4,  350);
	playSound(soundDuration, midi + 10, 350);
	playSound(soundDuration, midi + 18, 500);
}

function drawpie(digits, which) {
	let c = document.getElementById("myCanvas");
	let ctx = c.getContext("2d");
	ctx.clearRect(0, 0, c.width, c.height);
	ctx.beginPath();

	playSound(0.1, 80, 0);

	const the_date = new Date();

	let last_time = our_start_time;

	for (let k=0; k < digits.length - 3; k++) {

		// Lines
		if (which == 0 || which == 1) {
			ctx.moveTo(digits[k] * 50,   digits[k+1] * 50);
			ctx.lineTo(digits[k+2] * 50, digits[k+3] * 50);
			ctx.arc(digits[k]*50, digits[k+1]*50, digits[k+2]*50, digits[k+3] * 50, 2*Math.PI);
			ctx.stroke();
		}

		// Rectangles filled with gradient
		if (which == 1 || which == 2) {
			const grd = ctx.createLinearGradient(digits[k] * 50, digits[k+1] * 50, digits[k+2] * 50, digits[k+3] * 50);
			grd.addColorStop(0, "red");
			grd.addColorStop(0.33, "yellow");
			grd.addColorStop(0.67, "green");
			grd.addColorStop(1, "blue");
			ctx.fillStyle = grd;
			ctx.fillRect(digits[k] * 50, digits[k+1] * 50, digits[k+2] * 50, digits[k+3] * 50);
		}

		// Sound
		const a = ((digits[k].valueOf() * 10.0) -   -digits[k+1].valueOf()) * 0.01;
		const b = ((digits[k+2].valueOf() * 10.0) - -digits[k+3].valueOf()) * 0.01;

		if (which == 1 || which == 2) {
			playNoise(2.0 * a, Math.floor(88 * b), last_time + (a * 500));
		}

		if (which == 0 || which == 1) {
			playSound(2.0 * b, Math.floor(88 * a), last_time + (b * 500));
		}

		last_time += 250;

	}
	our_start_time = audioContext.currentTime;
}

function find_in(n, a) {
	for (let k = 0; k < a.length; k++) {
		if (a[k] == n) return k;
	}
	return -1;
}

function calculate(which) {
	const max_rational = 10000000;

	const rational = parseInt(document.getElementById("rational_in").value);
	if ((rational < 1) || (rational > max_rational) || isNaN(rational)) return;

	let digits = "";
	let rem = 1;
	let k = rational;
	let num = 1;
	let last_rem = 0;
	let already_used = [];
	let where_found = -777;

	already_used.push(1);

	while (true) {
		let ct = 0;

		while (rem < k) {
			rem *= 10;
			ct++;
			if (ct > 1) digits += "0";
		}
		num = Math.floor(rem / k);
		digits += num.toString();

		document.getElementById("digits").innerHTML = digits;

		if (digits.length > max_rational) break;

		document.getElementById("length").innerHTML = digits.length;
		rem -= num * k;

		if (already_used.length > 0) where_found = find_in(rem, already_used);

		if ((rem < 1) || (where_found > -1)) break;

		last_rem = rem;
		already_used.push(rem);
	}

	if (where_found > -1) {
		let mask = "";
		for (let k = 0; k < where_found; k++) {
			mask += "|";
		}
		for (let k = where_found; k < digits.length; k++) {
			mask += "_";
		}
		document.getElementById("mask").innerHTML = mask;
		document.getElementById("repeat_from").innerHTML = where_found + 1;
	}

	drawpie(digits, which);
}
