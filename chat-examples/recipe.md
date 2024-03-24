## Appendix A: Recipe Examples

**I am trying to preprocess Landsat 8 Level-1 data. I know that I need to find and download the data. I know that I need to complete georeferencing, conversion to radiance, solar corrections and atmospheric corrections. I know I will use the ENVI software. Please provide a complete sequence of steps. Please fill in any missing steps. \[March 15, 2024\]**

ChatGPT

Preprocessing Landsat 8 Level-1 data involves several steps to ensure accurate and usable data for analysis. Here's a complete sequence of steps:

- Data Acquisition and Download:
  - Visit the USGS EarthExplorer website or other reliable sources for Landsat data.
  - Select Landsat 8 as the satellite and define the area and time period you're interested in.
  - Download the Level-1 data for the desired scene.
- Data Preparation:
  - Extract the downloaded data to a dedicated folder on your computer.
- Georeferencing:
  - Use ENVI's georeferencing tools to ensure that the image is properly aligned with a known coordinate system.
  - Choose ground control points (GCPs) from a reliable source such as a georeferenced base map or high-resolution imagery.
  - Perform the georeferencing process and save the output.
- Conversion to Radiance:
  - Open the georeferenced Landsat 8 image in ENVI.
  - Use the metadata provided with the image to convert digital numbers (DN) to radiance values.
  - Apply the appropriate conversion coefficients provided by the Landsat documentation for each spectral band.
- Solar Corrections:
  - Calculate solar angles for the acquisition date and time using tools within ENVI or external software.
  - Apply the appropriate correction factors to adjust for variations in solar irradiance at the time of image acquisition.
  - Ensure consistency across all spectral bands.
- Atmospheric Corrections:
  - Perform atmospheric correction to remove the effects of atmospheric scattering and absorption.
  - Use ENVI's atmospheric correction tools or external software such as FLAASH or QUAC to apply corrections.
  - Select an appropriate atmospheric model (e.g., MODTRAN) and input parameters such as aerosol optical depth and water vapor content.
- Additional Processing (Optional):
  - Conduct additional processing steps such as image sharpening, noise reduction, or spectral enhancement based on the specific requirements of your analysis.
- Data Export:
  - Export the preprocessed Landsat data to a format suitable for further analysis, such as GeoTIFF or ENVI raster format.
  - Ensure that the exported data retains the necessary geospatial information for accurate interpretation and analysis.
- Quality Assessment:
  - Perform a visual and quantitative assessment of the preprocessed data to ensure that it meets your quality standards.
  - Check for artifacts, anomalies, or inconsistencies that may affect the accuracy of your analysis.
- Documentation:
  - Document the preprocessing steps undertaken, including parameter settings, software used, and any adjustments made to the data.
  - Maintain metadata associated with the preprocessed data to facilitate reproducibility and data sharing.

By following these steps, you should be able to preprocess Landsat 8 Level-1 data effectively for your intended analysis.

**I am trying to find and download infrared data of the Crab Nebula. I know that I need to identify the various coordinates of the Crab Nebula. I know that I need to search for data across a number of astronomical catalogs. Please provide a complete sequence of steps. Please fill in any missing steps. \[March 15, 2024\]**

ChatGPT

Sure, here's a complete sequence of steps to find and download infrared data of the Crab Nebula:

- Identify Coordinates:
  - The Crab Nebula's coordinates are approximately:
    - Right Ascension (RA): 05h 34m 31.97s
    - Declination (Dec): +22° 00' 52.1"
- Choose an Astronomical Catalog:
  - Infrared data of celestial objects can be found in various catalogs. Some popular ones include:
    - NASA/IPAC Extragalactic Database (NED)
    - NASA Exoplanet Archive
    - SIMBAD Astronomical Database
    - VizieR Astronomical Catalog Service
- Access the Chosen Catalog:
  - Go to the website of the selected catalog.
- Search for the Crab Nebula:
  - Enter the coordinates of the Crab Nebula (RA and Dec) into the search bar or use the object name.
- Filter for Infrared Data:
  - After finding the Crab Nebula, filter the data to include only infrared observations. This can usually be done through advanced search options or filters.
- Select and Download Data:
  - Once you've filtered for infrared data, select the dataset or datasets you're interested in.
  - Follow the instructions on the website to download the data. This may involve creating an account or agreeing to certain terms and conditions.
- Verify Data Format and Compatibility:
  - Make sure the downloaded data is in a format compatible with your software or analysis tools. Common formats for astronomical data include FITS (Flexible Image Transport System) and ASCII tables.
- Process and Analyze Data (Optional):
  - If necessary, process and analyze the downloaded data using software like IRAF (Image Reduction and Analysis Facility), DS9 (SAOImage DS9), or Python libraries like Astropy.
- Visualize the Data:
  - Use visualization tools to view the infrared images or spectra obtained from the data. This could include software like Aladin, SAOImage DS9, or custom Python scripts.
- Interpret the Results:
  - Interpret the data to extract meaningful information about the Crab Nebula's infrared properties. This could involve comparing with data at other wavelengths or with theoretical models.
- Cite the Data Source:
  - If you're using the data for research or publication, make sure to properly cite the source of the data according to the guidelines provided by the catalog or dataset.

By following these steps, you should be able to find and download infrared data of the Crab Nebula from various astronomical catalogs.