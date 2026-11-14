/* 3D globe background for the countries page (/pays/).
 *
 * A dotted sphere turning slowly over Africa, the Blue Sky capitals as
 * orange markers and light pulses travelling along arcs from the head
 * office (Lubumbashi). Pure canvas, no library. Draws once and stops under
 * prefers-reduced-motion; pauses when the tab is hidden.
 */
(function () {
  "use strict";
  var canvas = document.querySelector("[data-globe3d]");
  if (!canvas || !canvas.getContext) return;
  var ctx = canvas.getContext("2d");
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var DEG = Math.PI / 180;
  var HUB = [-11.66, 27.48]; // Lubumbashi (head office)
  var CITIES = [
    [-4.32, 15.31],   // Kinshasa
    [-15.42, 28.28],  // Lusaka
    [-22.56, 17.08],  // Windhoek
    [-26.2, 28.05],   // Johannesburg
    [-17.83, 31.05],  // Harare
    [-1.29, 36.82],   // Nairobi
    [0.35, 32.58],    // Kampala
    [-6.79, 39.28],   // Dar es Salaam
    [-13.96, 33.79],  // Lilongwe
  ];

  // Points evenly spread on a sphere (Fibonacci lattice).
  var N = 2400, points = [];
  var golden = Math.PI * (3 - Math.sqrt(5));
  for (var i = 0; i < N; i++) {
    var y = 1 - (i / (N - 1)) * 2, r = Math.sqrt(1 - y * y), th = golden * i;
    points.push([Math.cos(th) * r, y, Math.sin(th) * r]);
  }

  function fromLatLon(lat, lon, lift) {
    var la = lat * DEG, lo = lon * DEG, rr = 1 + (lift || 0);
    return [rr * Math.cos(la) * Math.sin(lo), rr * Math.sin(la), rr * Math.cos(la) * Math.cos(lo)];
  }

  // Great-circle arc from the hub to each city, lifted above the surface.
  function arc(a, b, steps) {
    var A = fromLatLon(a[0], a[1]), Bv = fromLatLon(b[0], b[1]), out = [];
    var dot = A[0] * Bv[0] + A[1] * Bv[1] + A[2] * Bv[2];
    var om = Math.acos(Math.max(-1, Math.min(1, dot))) || 1e-6;
    for (var s = 0; s <= steps; s++) {
      var t = s / steps, k1 = Math.sin((1 - t) * om) / Math.sin(om), k2 = Math.sin(t * om) / Math.sin(om);
      var lift = 1 + Math.sin(Math.PI * t) * (0.08 + om * 0.25);
      out.push([(A[0] * k1 + Bv[0] * k2) * lift, (A[1] * k1 + Bv[1] * k2) * lift, (A[2] * k1 + Bv[2] * k2) * lift]);
    }
    return out;
  }
  var arcs = CITIES.map(function (c) { return arc(HUB, c, 48); });
  var markers = [HUB].concat(CITIES).map(function (c) { return fromLatLon(c[0], c[1], 0.004); });

  var W = 0, H = 0, R = 0, cx = 0, cy = 0, dpr = 1;
  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = canvas.clientWidth; H = canvas.clientHeight;
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    var mobile = W < 768;
    R = mobile ? Math.min(W * 0.7, H * 0.4) : Math.min(W * 0.34, H * 0.62);
    cx = mobile ? W * 0.55 : W * 0.5;
    cy = mobile ? H * 0.42 : H * 0.6;
  }

  // Rotation: turn around Africa (lon ~10..40E) with a gentle swing, plus
  // a small tilt following the pointer / device.
  var tiltX = 0, tiltY = 0, targetX = 0, targetY = 0;
  window.addEventListener("pointermove", function (e) {
    targetY = (e.clientX / window.innerWidth - 0.5) * 0.35;
    targetX = (e.clientY / window.innerHeight - 0.5) * 0.25;
  }, { passive: true });
  window.addEventListener("deviceorientation", function (e) {
    if (e.gamma == null) return;
    targetY = Math.max(-1, Math.min(1, e.gamma / 45)) * 0.3;
    targetX = Math.max(-1, Math.min(1, (e.beta - 45) / 45)) * 0.2;
  }, { passive: true });

  function project(p, rotY, rotX) {
    var cosY = Math.cos(rotY), sinY = Math.sin(rotY), cosX = Math.cos(rotX), sinX = Math.sin(rotX);
    var x = p[0] * cosY - p[2] * sinY, z = p[0] * sinY + p[2] * cosY, y = p[1];
    var y2 = y * cosX - z * sinX, z2 = y * sinX + z * cosX;
    var persp = 2.6 / (2.6 - z2);
    return [cx + x * R * persp, cy - y2 * R * persp, z2, persp];
  }

  function draw(time) {
    var t = time / 1000;
    tiltX += (targetX - tiltX) * 0.04; tiltY += (targetY - tiltY) * 0.04;
    var rotY = 27 * DEG + Math.sin(t * 0.12) * 0.35 + tiltY;   // Africa (around 27°E) faces the viewer
    var rotX = -12 * DEG + tiltX;
    ctx.clearRect(0, 0, W, H);

    // Soft halo behind the globe.
    var halo = ctx.createRadialGradient(cx, cy, R * 0.2, cx, cy, R * 1.35);
    halo.addColorStop(0, "rgba(29,78,216,0.10)");
    halo.addColorStop(1, "rgba(29,78,216,0)");
    ctx.fillStyle = halo; ctx.beginPath(); ctx.arc(cx, cy, R * 1.35, 0, Math.PI * 2); ctx.fill();

    // Sphere body: light from the top-left gives it volume, plus a thin rim.
    var body = ctx.createRadialGradient(cx - R * 0.35, cy - R * 0.4, R * 0.1, cx, cy, R * 1.05);
    body.addColorStop(0, "rgba(255,255,255,0.55)");
    body.addColorStop(0.55, "rgba(219,234,254,0.35)");
    body.addColorStop(1, "rgba(29,78,216,0.16)");
    ctx.fillStyle = body; ctx.beginPath(); ctx.arc(cx, cy, R * 1.02, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = "rgba(29,78,216,0.22)"; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.arc(cx, cy, R * 1.02, 0, Math.PI * 2); ctx.stroke();

    // Dots: brighter and bigger on the side facing us.
    for (var i = 0; i < points.length; i++) {
      var q = project(points[i], rotY, rotX);
      var front = (q[2] + 1) / 2;
      ctx.fillStyle = "rgba(29,78,216," + (0.04 + front * front * 0.78).toFixed(3) + ")";
      var s = (0.7 + front * 2.1) * q[3];
      ctx.fillRect(q[0] - s / 2, q[1] - s / 2, s, s);
    }

    // Arcs with a pulse travelling from the hub.
    for (var a = 0; a < arcs.length; a++) {
      var pts = arcs[a].map(function (p) { return project(p, rotY, rotX); });
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      for (var k = 0; k < pts.length; k++) {
        if (k === 0) ctx.moveTo(pts[k][0], pts[k][1]); else ctx.lineTo(pts[k][0], pts[k][1]);
      }
      var vis = pts[Math.floor(pts.length / 2)][2] > -0.2 ? 0.45 : 0.12;
      ctx.strokeStyle = "rgba(255,164,86," + vis + ")";
      ctx.stroke();
      if (!reduce) {
        var phase = ((t * 0.32 + a / arcs.length) % 1), idx = Math.floor(phase * (pts.length - 1)), p = pts[idx];
        if (p[2] > -0.3) {
          ctx.fillStyle = "rgba(255,164,86,0.95)";
          ctx.beginPath(); ctx.arc(p[0], p[1], 2.6 * p[3], 0, Math.PI * 2); ctx.fill();
        }
      }
    }

    // City markers (hub larger, pulsing ring).
    for (var m = 0; m < markers.length; m++) {
      var c = project(markers[m], rotY, rotX);
      if (c[2] < -0.15) continue;
      var size = (m === 0 ? 5 : 3.4) * c[3];
      ctx.fillStyle = m === 0 ? "#f2914a" : "#ffa456";
      ctx.beginPath(); ctx.arc(c[0], c[1], size, 0, Math.PI * 2); ctx.fill();
      if (!reduce) {
        var ring = (t * 0.8 + m * 0.37) % 1;
        ctx.strokeStyle = "rgba(255,164,86," + (0.5 * (1 - ring)).toFixed(3) + ")";
        ctx.lineWidth = 1.2;
        ctx.beginPath(); ctx.arc(c[0], c[1], size + ring * 14, 0, Math.PI * 2); ctx.stroke();
      }
    }
  }

  var running = false;
  function loop(time) {
    if (!running) return;
    draw(time);
    requestAnimationFrame(loop);
  }
  function start() { if (!running && !reduce) { running = true; requestAnimationFrame(loop); } }
  function stop() { running = false; }

  resize();
  window.addEventListener("resize", function () { resize(); if (reduce) draw(0); });
  document.addEventListener("visibilitychange", function () { document.hidden ? stop() : start(); });
  if (reduce) { draw(0); } else { start(); }
})();
