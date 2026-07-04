/**
 * Stylised SVG track library for the F1 season simulator.
 *
 * Each track exports:
 *   - path: SVG path in a 1000x600 viewBox
 *   - name: display label
 *   - country: 2-letter country code / short tag
 *   - clockwise: boolean (currently only affects the direction of the animation)
 *
 * These are NOT geographically accurate maps — they are recognisable
 * caricatures of each circuit's essential shape (long straights, tight
 * hairpins, banking, figure-eight...) so that the player can tell them apart.
 */

// ---------------------------------------------------------------------------
// Hand-drawn iconic circuits
// ---------------------------------------------------------------------------
const TRACKS = {
  Monaco: {
    // Tight, compact, twisty — harbor loop
    name: "Monaco",
    country: "MC",
    clockwise: true,
    path:
      "M 200 380 L 250 380 C 300 380 320 350 320 310 L 320 250 C 320 210 350 190 400 190 L 500 190 C 540 190 560 200 570 230 L 590 280 C 600 310 630 320 660 300 L 720 260 C 750 240 780 240 800 270 L 820 310 C 830 340 820 370 790 385 L 720 415 C 700 425 690 445 700 465 L 720 500 C 730 520 720 540 690 545 L 260 545 C 220 545 200 525 200 490 Z",
  },

  Monza: {
    // Long straights + Parabolica; "Cathedral of Speed"
    name: "Monza",
    country: "IT",
    clockwise: true,
    path:
      "M 120 460 L 780 460 C 850 460 890 430 890 380 C 890 330 850 300 780 300 L 720 300 C 700 300 690 285 690 265 L 690 200 C 690 170 670 150 640 150 L 300 150 C 250 150 220 170 210 210 L 190 260 C 180 280 165 290 145 290 L 130 290 C 105 290 90 305 90 330 L 90 430 C 90 450 100 460 120 460 Z",
  },

  "Spa-Francorchamps": {
    // Long elongated, with the iconic Eau Rouge/Raidillon kink
    name: "Spa",
    country: "BE",
    clockwise: true,
    path:
      "M 80 420 L 200 420 C 230 420 240 400 240 375 L 240 340 C 240 300 270 280 310 285 L 380 300 C 410 306 430 295 440 270 L 470 200 C 485 165 520 150 560 165 L 720 220 C 780 240 810 280 800 330 L 780 390 C 770 425 740 445 700 440 L 500 415 C 470 411 450 425 445 450 L 435 490 C 425 520 400 535 370 530 L 130 500 C 95 495 80 475 80 445 Z",
  },

  Silverstone: {
    // Home of British GP; flowing high-speed
    name: "Silverstone",
    country: "GB",
    clockwise: true,
    path:
      "M 120 380 C 120 320 160 280 220 275 L 340 265 C 380 262 400 240 405 210 L 415 160 C 425 130 450 115 485 120 L 620 145 C 670 155 700 190 700 240 L 700 290 C 700 320 720 340 750 345 L 830 355 C 870 361 895 390 895 425 C 895 470 865 495 820 495 L 250 495 C 175 495 120 455 120 400 Z",
  },

  Suzuka: {
    // Figure-eight (unique in F1)
    name: "Suzuka",
    country: "JP",
    clockwise: true,
    path:
      "M 120 320 C 120 250 180 210 260 220 L 400 245 C 450 254 480 285 470 320 C 460 355 415 375 370 365 L 260 340 C 205 328 155 355 155 400 C 155 450 210 480 275 470 L 460 445 C 520 437 555 460 570 495 L 590 555 M 470 320 C 480 285 530 260 590 265 L 780 285 C 850 293 895 335 890 395 C 885 455 830 495 760 490 L 660 485 C 610 482 585 510 590 555 Z",
  },

  Interlagos: {
    // Anti-clockwise, compact São Paulo circuit
    name: "Interlagos",
    country: "BR",
    clockwise: false,
    path:
      "M 800 200 L 720 200 C 680 200 650 220 640 260 L 620 320 C 610 355 580 375 545 370 L 400 350 C 355 344 320 365 310 405 L 295 460 C 285 495 255 515 220 510 L 130 495 C 95 490 80 470 85 440 L 100 350 C 105 320 130 300 165 300 L 240 300 C 275 300 300 280 305 250 L 315 200 C 325 175 350 160 380 165 L 780 220 Z",
  },

  Nurburgring: {
    // Modern GP layout (not the Nordschleife, kept compact)
    name: "Nürburgring",
    country: "DE",
    clockwise: true,
    path:
      "M 110 380 C 110 320 150 280 210 275 L 300 268 C 335 265 355 245 355 215 L 355 175 C 355 145 380 125 415 130 L 520 145 C 555 150 580 175 585 210 L 590 250 C 595 285 620 305 655 302 L 780 292 C 830 288 870 320 870 370 L 870 430 C 870 470 840 495 795 495 L 210 495 C 145 495 110 460 110 410 Z",
  },

  Sakhir: {
    // Bahrain — modern desert layout
    name: "Sakhir",
    country: "BH",
    clockwise: true,
    path:
      "M 110 460 L 340 460 C 375 460 395 445 400 415 L 410 355 C 415 320 440 300 475 305 L 610 325 C 645 330 665 315 670 285 L 680 220 C 688 185 715 165 750 170 L 830 180 C 870 186 895 215 890 255 L 875 385 C 870 425 840 450 800 450 L 700 450 C 675 450 660 465 660 490 L 660 520 C 660 540 645 555 620 555 L 145 555 C 115 555 105 540 105 515 Z",
  },

  Melbourne: {
    // Albert Park — around a lake, gentle curves
    name: "Melbourne",
    country: "AU",
    clockwise: true,
    path:
      "M 120 380 C 120 300 180 250 260 250 L 480 250 C 560 250 610 275 640 320 L 690 400 C 720 445 770 470 820 465 C 870 460 895 435 890 400 L 875 300 C 870 260 845 235 810 235 L 300 155 C 220 145 155 195 130 275 Z",
  },

  Barcelona: {
    // Circuit de Catalunya — very balanced technical layout
    name: "Barcelona",
    country: "ES",
    clockwise: true,
    path:
      "M 120 460 L 780 460 C 830 460 860 435 860 395 L 860 320 C 860 290 840 275 810 275 L 700 275 C 670 275 655 260 655 235 L 655 180 C 655 155 635 140 605 140 L 320 140 C 285 140 260 160 250 195 L 235 240 C 225 275 200 295 165 295 L 130 295 C 105 295 90 310 90 335 L 90 435 C 90 455 105 460 120 460 Z",
  },

  Hungaroring: {
    // "Monaco without walls" — twisty
    name: "Hungaroring",
    country: "HU",
    clockwise: true,
    path:
      "M 130 400 C 130 340 175 300 240 302 L 370 308 C 405 310 425 295 430 265 L 440 205 C 448 175 470 158 500 165 L 590 185 C 620 192 635 210 630 240 L 620 285 C 615 315 635 335 665 335 L 780 335 C 830 335 860 365 860 410 C 860 455 830 485 780 485 L 220 485 C 155 485 130 455 130 415 Z",
  },

  Zandvoort: {
    // Dutch coast — banked, flowing bowl
    name: "Zandvoort",
    country: "NL",
    clockwise: true,
    path:
      "M 150 380 C 150 300 200 250 280 245 L 500 235 C 580 230 630 260 655 320 L 690 400 C 715 450 760 475 810 470 C 860 465 890 435 890 395 L 890 310 C 890 260 855 230 800 235 L 550 250 C 500 253 470 235 465 200 L 460 155 C 455 130 435 115 405 120 L 220 145 C 175 152 150 175 145 215 Z",
  },

  Imola: {
    // Anti-clockwise Italian classic
    name: "Imola",
    country: "IT",
    clockwise: false,
    path:
      "M 850 320 L 780 320 C 745 320 725 340 720 375 L 715 420 C 710 460 680 485 640 485 L 220 485 C 160 485 120 455 120 410 L 120 320 C 120 275 155 245 205 245 L 340 245 C 380 245 400 225 405 195 L 415 155 C 425 125 450 108 485 115 L 720 155 C 770 163 800 190 810 235 L 850 320 Z",
  },

  "Marina Bay": {
    // Singapore — night street circuit, right-angled
    name: "Marina Bay",
    country: "SG",
    clockwise: false,
    path:
      "M 120 200 L 400 200 L 400 260 L 550 260 L 550 190 L 700 190 L 700 300 L 830 300 L 830 400 L 720 400 L 720 470 L 550 470 L 550 420 L 380 420 L 380 500 L 200 500 L 200 400 L 120 400 Z",
  },

  Baku: {
    // Azerbaijan — long straight + castle section
    name: "Baku",
    country: "AZ",
    clockwise: false,
    path:
      "M 100 450 L 780 450 C 820 450 845 425 845 390 L 845 340 C 845 305 820 285 785 285 L 700 285 L 700 220 L 650 220 L 650 180 L 500 180 L 500 250 L 320 250 L 320 200 L 240 200 L 240 260 L 160 260 L 160 340 L 100 340 Z",
  },

  Austin: {
    // COTA — turn 1 climb + Esses signature
    name: "Austin (COTA)",
    country: "US",
    clockwise: false,
    path:
      "M 120 500 L 300 500 C 340 500 360 480 365 445 L 375 380 C 380 345 405 325 440 330 L 520 340 C 550 344 570 330 575 305 L 585 250 C 595 215 625 195 660 205 L 780 235 C 830 248 860 285 855 330 L 840 420 C 835 460 805 485 765 480 L 620 465 C 590 462 570 478 565 505 L 560 530 C 555 550 540 560 520 555 L 150 545 C 125 542 115 528 118 510 Z",
  },

  Shanghai: {
    // Shape based on Chinese character "shang" — snail spiral
    name: "Shanghai",
    country: "CN",
    clockwise: true,
    path:
      "M 500 130 C 570 130 620 170 620 240 C 620 300 580 340 520 340 C 480 340 450 315 450 275 C 450 245 470 225 500 225 C 520 225 535 240 535 260 M 500 130 C 350 130 260 200 260 320 C 260 430 350 500 480 500 L 780 500 C 830 500 860 470 860 425 L 860 370 C 860 320 825 290 775 295 L 700 305 C 660 310 640 290 640 260",
  },

  Sepang: {
    // Malaysia — two long straights, sweeping corners
    name: "Sepang",
    country: "MY",
    clockwise: true,
    path:
      "M 130 220 L 340 220 C 380 220 400 240 400 275 L 400 340 C 400 375 425 395 460 395 L 720 395 C 760 395 785 375 790 340 L 800 260 C 808 220 840 195 880 205 L 890 300 C 895 350 870 385 830 400 L 500 480 C 400 500 320 470 260 405 L 155 300 C 130 275 115 250 130 220 Z",
  },

  Spielberg: {
    // Red Bull Ring — short, elevation
    name: "Spielberg",
    country: "AT",
    clockwise: true,
    path:
      "M 140 460 C 140 400 180 360 240 355 L 400 340 C 435 337 455 320 460 290 L 470 230 C 480 195 510 175 545 185 L 720 235 C 770 250 795 285 785 330 L 770 400 C 760 440 730 465 690 460 L 230 445 C 175 442 140 445 140 460 Z",
  },

  Jeddah: {
    // Saudi Arabia — very fast street circuit, flowing
    name: "Jeddah",
    country: "SA",
    clockwise: false,
    path:
      "M 100 380 L 240 380 C 270 380 285 400 285 425 L 285 470 C 285 495 305 510 335 505 L 500 480 C 540 475 560 490 570 520 L 585 555 M 100 380 C 100 300 145 260 220 260 L 400 260 C 440 260 460 240 465 210 L 475 165 C 485 130 515 115 550 125 L 800 195 C 850 210 880 245 875 290 L 860 400 C 850 440 815 460 775 452 L 640 430 C 605 425 590 440 585 470 L 585 555 Z",
  },

  Miami: {
    // Miami — snakey around a stadium
    name: "Miami",
    country: "US",
    clockwise: false,
    path:
      "M 130 480 L 300 480 C 340 480 360 460 365 425 L 380 340 C 385 305 410 285 445 290 L 555 305 C 590 310 610 295 615 265 L 625 210 C 635 180 660 165 690 175 L 790 205 C 830 218 855 250 850 285 L 830 405 C 825 445 795 470 755 465 L 145 460 C 125 458 118 470 130 480 Z",
  },

  Indianapolis: {
    // Iconic oval
    name: "Indianapolis",
    country: "US",
    clockwise: false,
    path:
      "M 200 200 L 800 200 C 860 200 890 240 890 300 C 890 360 860 400 800 400 L 200 400 C 140 400 110 360 110 300 C 110 240 140 200 200 200 Z",
  },

  "Yas Marina": {
    // Abu Dhabi — under-hotel section
    name: "Yas Marina",
    country: "AE",
    clockwise: false,
    path:
      "M 120 460 L 300 460 C 335 460 355 445 360 415 L 370 355 C 375 320 400 300 435 305 L 550 320 C 585 325 605 310 610 285 L 620 220 C 630 190 655 175 685 185 L 810 220 C 855 232 880 265 875 305 L 860 410 C 855 445 830 465 795 460 L 155 445 C 130 442 115 450 120 460 Z",
  },

  Montreal: {
    // Circuit Gilles Villeneuve — island, kinky
    name: "Montréal",
    country: "CA",
    clockwise: true,
    path:
      "M 100 300 L 300 300 L 300 240 L 500 240 L 500 200 L 700 200 C 750 200 780 225 785 270 L 800 380 C 805 425 780 460 735 465 L 550 470 L 550 430 L 380 430 L 380 470 L 200 470 C 145 470 105 435 100 380 Z",
  },

  Hockenheim: {
    // Post-2002 shortened layout
    name: "Hockenheim",
    country: "DE",
    clockwise: true,
    path:
      "M 130 420 C 130 355 175 310 240 305 L 380 295 C 415 293 435 275 440 245 L 450 195 C 460 165 485 148 515 155 L 620 180 C 660 190 680 220 675 260 L 665 305 C 660 335 685 355 715 355 L 810 355 C 855 355 880 385 875 425 C 870 465 840 490 800 485 L 220 475 C 160 470 130 450 130 425 Z",
  },

  Estoril: {
    // Portugal
    name: "Estoril",
    country: "PT",
    clockwise: true,
    path:
      "M 130 380 C 130 320 165 285 220 285 L 340 285 C 375 285 395 265 400 235 L 415 175 C 425 145 450 130 480 140 L 740 210 C 790 225 815 260 805 305 L 785 400 C 775 440 745 465 705 460 L 220 445 C 160 440 130 420 130 395 Z",
  },

  Adelaide: {
    // Street circuit
    name: "Adelaide",
    country: "AU",
    clockwise: false,
    path:
      "M 100 200 L 800 200 L 800 300 L 700 300 L 700 400 L 800 400 L 800 500 L 400 500 L 400 400 L 200 400 L 200 300 L 100 300 Z",
  },

  Kyalami: {
    // South Africa
    name: "Kyalami",
    country: "ZA",
    clockwise: true,
    path:
      "M 130 460 C 130 400 170 360 230 355 L 400 345 C 440 342 460 320 460 285 L 460 200 C 460 165 485 145 520 150 L 750 200 C 800 210 830 250 820 300 L 800 400 C 790 440 760 465 720 460 L 200 445 C 155 442 130 445 130 460 Z",
  },

  Mugello: {
    name: "Mugello",
    country: "IT",
    clockwise: true,
    path:
      "M 130 380 C 130 320 170 285 230 285 L 420 285 C 460 285 480 265 485 235 L 495 175 C 505 145 530 130 565 140 L 780 210 C 830 225 860 265 850 315 L 830 400 C 820 440 790 465 750 460 L 220 445 C 160 440 130 420 130 395 Z",
  },

  Portimao: {
    name: "Portimão",
    country: "PT",
    clockwise: true,
    path:
      "M 130 400 C 130 320 175 275 250 275 L 400 275 C 435 275 455 255 460 220 L 470 175 C 480 145 505 128 540 140 L 720 200 C 770 217 795 250 785 300 L 765 400 C 755 440 725 465 685 460 L 220 445 C 155 440 125 420 130 395 Z",
  },

  Sochi: {
    name: "Sochi",
    country: "RU",
    clockwise: false,
    path:
      "M 130 460 L 620 460 L 620 400 L 750 400 L 750 300 L 830 300 L 830 200 L 500 200 L 500 260 L 300 260 L 300 320 L 150 320 Z",
  },

  Istanbul: {
    name: "Istanbul Park",
    country: "TR",
    clockwise: false,
    path:
      "M 130 380 C 130 320 165 285 220 285 L 380 285 C 415 285 435 265 440 235 L 450 180 C 460 148 485 130 520 140 L 730 200 C 780 217 810 260 800 310 L 785 400 C 775 440 745 465 705 460 L 220 445 C 160 440 130 420 130 395 Z",
  },
};

// ---------------------------------------------------------------------------
// Procedural fallback shapes — used when the circuit has no hand-drawn map.
// Each template has a different overall silhouette (blocky, curvy, tri-lobed).
// ---------------------------------------------------------------------------
const FALLBACK_TEMPLATES = [
  // Rounded rectangle with kink
  "M 140 200 L 700 200 C 780 200 830 260 830 320 L 830 400 C 830 460 790 490 730 490 L 300 490 C 220 490 130 470 130 400 L 130 260 C 130 220 130 200 140 200 Z",
  // Peanut-shape
  "M 150 300 C 150 200 240 160 340 200 L 500 260 C 580 290 700 240 780 240 C 860 240 890 320 850 400 C 810 480 700 500 600 460 L 400 400 C 300 360 200 460 150 400 Z",
  // Slanted triangle
  "M 130 480 L 780 460 C 830 458 860 430 850 390 L 810 240 C 800 205 770 185 730 195 L 260 320 C 200 335 140 400 130 480 Z",
  // Two-lobe
  "M 130 350 C 130 260 190 220 280 240 L 420 275 C 460 285 490 265 495 235 C 500 205 530 190 565 200 L 780 260 C 850 280 880 340 850 400 L 800 460 C 770 490 720 490 690 460 L 550 380 C 510 360 470 380 460 415 L 440 470 C 420 495 380 500 350 480 L 180 400 C 145 385 130 375 130 350 Z",
  // Long straight bottom + tight top
  "M 130 470 L 800 470 C 850 470 875 445 870 405 L 855 300 C 850 260 820 240 780 245 L 500 275 C 460 280 440 265 435 235 L 425 190 C 415 160 385 145 355 160 L 200 220 C 150 245 130 285 130 340 Z",
  // Small oval with dogleg
  "M 200 250 L 720 250 C 800 250 850 300 850 370 C 850 440 800 490 720 490 L 400 490 C 340 490 300 460 300 400 L 300 360 C 300 320 260 290 200 290 L 140 290 C 100 290 90 260 130 250 Z",
];

const hash = (s = "") => {
  let h = 0;
  for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0;
  return Math.abs(h);
};

export const getTrack = (circuitName) => {
  if (!circuitName) return { path: FALLBACK_TEMPLATES[0], name: "Circuit", country: "" };
  // exact match
  if (TRACKS[circuitName]) return TRACKS[circuitName];
  // fuzzy: lowercase compare
  const lc = circuitName.toLowerCase();
  for (const k of Object.keys(TRACKS)) {
    if (k.toLowerCase() === lc) return TRACKS[k];
  }
  // partial keyword match (e.g. "Spa" in "Spa-Francorchamps")
  for (const k of Object.keys(TRACKS)) {
    if (
      lc.includes(k.toLowerCase()) ||
      k.toLowerCase().includes(lc.split(" ")[0])
    ) {
      return TRACKS[k];
    }
  }
  // procedural fallback
  const idx = hash(circuitName) % FALLBACK_TEMPLATES.length;
  return {
    path: FALLBACK_TEMPLATES[idx],
    name: circuitName,
    country: "",
    clockwise: hash(circuitName) % 2 === 0,
  };
};

// ---------------------------------------------------------------------------
// Real F1 lap counts (recent/typical) per circuit. Fallback = 60.
// Historical circuits use approximate historical counts.
// ---------------------------------------------------------------------------
const LAP_COUNTS = {
  Monaco: 78,
  Monza: 53,
  "Spa-Francorchamps": 44,
  Silverstone: 52,
  Suzuka: 53,
  Interlagos: 71,
  Nurburgring: 60,
  Sakhir: 57,
  Melbourne: 58,
  Barcelona: 66,
  Hungaroring: 70,
  Zandvoort: 72,
  Imola: 63,
  "Marina Bay": 62,
  Baku: 51,
  Austin: 56,
  Shanghai: 56,
  Sepang: 56,
  Spielberg: 71,
  Jeddah: 50,
  Miami: 57,
  Indianapolis: 73,
  "Yas Marina": 58,
  Montreal: 70,
  Hockenheim: 67,
  Estoril: 71,
  Adelaide: 82,
  Kyalami: 78,
  Mugello: 59,
  Portimao: 66,
  Sochi: 53,
  Istanbul: 58,
  // Historical / retired circuits (approximate)
  Reims: 60,
  Aintree: 90,
  Sebring: 42,
  "Watkins Glen": 108,
  "East London": 82,
  Riverside: 75,
  Rouen: 90,
  "Mexico City": 71,
  "Clermont-Ferrand": 38,
  "Brands Hatch": 76,
  Jarama: 75,
  "Long Beach": 80,
  Zolder: 70,
  Detroit: 63,
  "Paul Ricard": 53,
  Osterreichring: 54,
  "Buenos Aires": 72,
  "Magny-Cours": 70,
  Losail: 57,
  "Las Vegas": 50,
};

export const getLapCount = (circuitName) => {
  if (!circuitName) return 60;
  if (LAP_COUNTS[circuitName]) return LAP_COUNTS[circuitName];
  const lc = circuitName.toLowerCase();
  for (const k of Object.keys(LAP_COUNTS)) {
    if (k.toLowerCase() === lc) return LAP_COUNTS[k];
    if (
      lc.includes(k.toLowerCase()) ||
      k.toLowerCase().includes(lc.split(" ")[0])
    ) {
      return LAP_COUNTS[k];
    }
  }
  // Deterministic pseudo-random default per circuit (44-72)
  return 44 + (hash(circuitName) % 29);
};

export default getTrack;
