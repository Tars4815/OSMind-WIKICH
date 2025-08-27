# OSMInd-WikiCH

**Crowdsourced Indoor Mapping and Semantic Enrichment for Cultural Heritage**

This repository hosts the code and workflow for creating lightweight, interactive 3D prototype for virtual tours of cultural heritage buildings by integrating **OpenStreetMap (OSM)** indoor data with **Wikidata** semantic enrichment. The project demonstrates how open geodata and linked open data can be combined in a fully open-source pipeline to provide interactive and accessible cultural heritage experiences.

Developed as part of the work presented at **CIPA 2025 – Seoul**.

**This repository contains code and document of a work that is under development**

---

## Features

- Extracts indoor features (rooms, walls, doors, artworks, POIs) from **OSM** using the **QuickOSM** plugin in QGIS.  
- Processes and validates geometry/topology consistency with a **PyQGIS script** (via `modello.model3` or alternative `data-processing.py`).  
- Generates interactive **3D indoor scenes** using the **Qgis2threejs** plugin.  
- Integrates **Wikidata** properties and media via API, enabling real-time semantic pop-ups (title, author, material, image, etc.).  
- Publishes the resulting viewer online with **GitHub Pages**.  
- Fully open and reproducible workflow, adaptable for museums and cultural institutions.  

---

## Repository Structure

```
OSMind-WIKICH/
│
├── app/ # Web viewer files (HTML, CSS, JS) exported from Qgis2threejs and customised
├── data/ # Sample datasets or processed layers (if included)
├── model3/ # QGIS Model Designer workflow for automated processing
├── data-processing.py # Alternative PyQGIS script (customisable, can be run in QGIS console)
├── docs/ # Documentation for GitHub Pages deployment
└── README.md # Project documentation
```

## Requirements

To run and adapt this workflow, you need:  
- **QGIS 3.x**  
- QGIS plugin **QuickOSM** (for Overpass API queries)  
- QGIS plugin **Qgis2threejs** (for 3D export and web viewer generation)  
- A **GitHub Pages** enabled repository (for publishing the interactive viewer)

## Getting started

### 1. Clone this repository

```
git clone https://github.com/Tars4815/OSMind-WIKICH.git
cd OSMind-WIKICH

```

### 2. Download indoor OSM data

- Open QGIS

- Use the QuickOSM plugin to query indoor features (e.g. indoor=*, exhibit=*, wikidata=*) for your case study building.

### 3. Process the dataset

- *Option A*: Run the provided Model Designer workflow in model3/

- *Option B* (alternative, more customisable): Run data-processing.py in the QGIS Python Console

This step checks geometry consistency (e.g. overlapping polygons, misaligned features) and prepares layers for 3D rendering.

### 4. Generate the 3D viewer

- Style and extrude features in QGIS
- Export the scene with Qgis2threejs
- Copy/export the generated HTML/JS files into the app/ folder

### 5. Link Wikidata

- Pop-up in the viewer dynamically fetch Wikidata information for artworks/POIs via their wikidata=* tag.

- Properties such as name, author, material, and images from Wikimedia Commons are automatically displayed.

### 6. Publish with GitHub Pages

- Push your code to GitHub

- Enable Pages in repository settings → your interactive 3D scene will be accessible via a shareable link.

## References

* Gaspari, F., Barbieri, F., Fascia, R., Pinto, L.: **Opportunities and challenges of Crowdsourced Indoor Geographic and Semantic Data for Built Heritage**, *Int. Arch. Photogramm. Remote Sens. Spatial Inf. Sci.*, CIPA 2025 conference proceedings to be published in August 2025. [Presentation slides available soon]

## License

This repository is released under the MIT License.
