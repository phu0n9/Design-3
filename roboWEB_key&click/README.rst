1. Make sure Flask is correctly installed.

2. Make sure runme.sh in this directory is executeable with:
chmod a+x runme.sh

3. Execute runme.sh as root or with sudo:
sudo ./runme.sh

4. Open a web browser and navigate to:
http://localhost:5000/

The index page should now display. The Google Maps boxes are just to demonstrate how the two iframes work -- this is a simple way to embed whatever scripts handle position tracking and video. You can build them as standalone seperate HTML pages and just link to them with the iframe.

NOTES:
The controls are just image links. When you click on them, they can execute Python code. An example is provided for the "forward" button. If you want to use javascript or similar to capture keypresses instead of using the image links, just make the javascript issue a GET request to the correct URL (e.g. localhost:5000/forward). 

VIDEO NOTES:

The URL where the video is accessible needs to be updated to include the IP address of the Raspberry Pi 3 on the local network. Probably the raspberry pi will need to have a static IP in the final version.
