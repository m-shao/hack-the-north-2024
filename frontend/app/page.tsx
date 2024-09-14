"use client";

import { useEffect, useRef, useState } from "react";
import {
  getMapData,
  show3dMap,
  TDirectionInstruction,
  Space,
  Directions,
  Marker,
} from "@mappedin/mappedin-js";
import "@mappedin/mappedin-js/lib/index.css";

interface Asset {
  name: string;
  image: string;
  color: string;
  step: number;
  originSpace: Space;
  destinationSpace?: Space;
  directions?: Directions;
  marker: Marker | undefined;
  currentInstruction: TDirectionInstruction | null;
}

const options = {
  key: "mik_Qar1NBX1qFjtljLDI52a60753",
  secret: "mis_CXFS9WnkQkzQmy9GCt4ucn2D68zNRgVa2aiJj5hEIFM8aa40fee",
  mapId: "66ce20fdf42a3e000b1b0545",
};

const Page = () => {

	const data = useRef(null)
  const [lastModified, setLastModified] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const checkFile = async () => {
      try {
        const response = await fetch('/data.json', {
          method: 'GET',
          headers: {
            'Cache-Control': 'no-cache', // Prevent caching
          },
        });

        if (response.ok) {
          const json = await response.json();
          const modified = response.headers.get('Last-Modified'); // Example of checking modification time

          if (lastModified !== modified) {
			if (!(data.current===json['message'])){
            data.current=json['message'];
			}
            setLastModified(modified);
          }
        } else {
          console.error('Failed to fetch data');
        }
      } catch (err) {
        setError(err);
      }
    };

    checkFile(); // Initial check

    const interval = setInterval(checkFile, 3000); // Poll every 3 seconds

    return () => clearInterval(interval); // Clean up interval on unmount
  }, [lastModified]); // Dependency on lastModified


 


  const mapRef = useRef<HTMLDivElement>(null);
  const [transcription, setTranscription] = useState<string>("");
  const [paused, setPaused] = useState<boolean>(false);
  const [currentDistance, setCurrentDistance] = useState<string>("");
  const [currentCoordinates, setCurrentCoordinates] = useState<{
    lat: number;
    lon: number;
  } | null>(null); // New state for real-time coordinates
  interface NearbyPOIs {
	front: string;
	back: string;
	left: string;
	right: string;
  }
  
  const [nearbyPOIs, setNearbyPOIs] = useState<String[]>([]); // State to store the nearby POIs

  const isPause = useRef<boolean>(false);

  function createGuardMarker(
    color: string = "#ffffff",
    label: string = "Contractor",
    image: string = ""
  ) {
    const html = `
    <div style="background-color: green; width: 10px; height: 10px; border-radius: 50%;"></div>
    `;
    return html;
  }

  function roundDistance(
    lat1: number | undefined,
    lon1: number | undefined,
    lat2: number | undefined,
    lon2: number | undefined
  ): number {
    if (!lat1 || !lon1 || !lat2 || !lon2) return 0;

    const R = 6371e3; // Radius of the Earth in meters
    const φ1 = (lat1 * Math.PI) / 180;
    const φ2 = (lat2 * Math.PI) / 180;
    const Δφ = ((lat2 - lat1) * Math.PI) / 180;
    const Δλ = ((lon2 - lon1) * Math.PI) / 180;

    const a =
      Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
      Math.cos(φ1) * Math.cos(φ2) * Math.sin(Δλ / 2) * Math.sin(Δλ / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    return Math.round(R * c);
  }

  async function init() {
    const mapData = await getMapData(options);
    const mapView = await show3dMap(mapRef.current as HTMLDivElement, mapData);

	const startPosition = 12;
	const spaces = await mapData.getByType("space");
	const endPosition = spaces.indexOf(spaces.find(item => item.name == data.current));
	console.log(endPosition)

  await spaces.forEach((space: Space,index:number) => {
    if (space.name && space.name.trim().length > 0) {
      mapView.Labels.add(space.center, space.name);  // Add label at the space center
    }
	
  });

  

    const assets: Asset[] = [];

 
    function updateAsset(a: Asset, duration: number) {
      if (!isPause.current) {
        if (!a.directions || a.directions.distance === 0) {
          a.destinationSpace = mapData.getByType("space")[endPosition];
          a.directions = mapView.getDirections(
            a.originSpace,
            a.destinationSpace
          );
          if (a.directions && a.directions.distance === 0) {
            return;
          }
        }
        const coordinate = a.directions?.coordinates[a.step];

        const distance = roundDistance(
          coordinate?.latitude,
          coordinate?.longitude,
          a.currentInstruction?.coordinate.latitude,
          a.currentInstruction?.coordinate.longitude
        );

        setCurrentDistance(`${distance} meters`);

        const foundInstruction = a.directions?.instructions.find(
          (instr) =>
            instr.coordinate.latitude === coordinate?.latitude &&
            instr.coordinate.longitude === coordinate?.longitude
        );
        const instruction = foundInstruction || a.currentInstruction;

        if (!coordinate || !instruction) return;

        if (foundInstruction) {
          setTranscription(
            `${instruction.action.type} ${
              instruction.action.bearing ?? ""
            } and walk ${Math.round(distance)} meters`
          );
          a.currentInstruction = instruction;
        }

        if (a.marker) {
          // Update the marker position using animateTo
          mapView.Markers.animateTo(a.marker, coordinate, {
            duration: duration,
            easing: "linear",
          });

          // Store and display the current position manually
          setCurrentCoordinates({
            lat: coordinate.latitude,
            lon: coordinate.longitude,
          });
        }

        if (a.directions && a.step >= a.directions.coordinates.length - 1) {
          setTranscription("Arrived");
        } else {
          a.step += 1;
        }
      }
    }

    function addAsset(name: string, image: string, color: string = "#0279FF") {
      const originSpace = mapData.getByType("space")[startPosition];
      const marker = mapView.Markers.add(
        originSpace,
        createGuardMarker(color, name, image),
        { rank: "always-visible" }
      );

      assets.push({
        name: name,
        image: image,
        color: color,
        originSpace: originSpace,
        marker: marker,
        step: 0,
        currentInstruction: null,
      });
    }

    addAsset("John", "");

    function updatePositions() {
      updateAsset(assets[0], 1000);
      setTimeout(updatePositions, 1500);
    }

    updatePositions();
  }

  function calculateBearing(lat1:number, lon1:number, lat2:number, lon2:number) {
	const φ1 = (lat1 * Math.PI) / 180;
	const φ2 = (lat2 * Math.PI) / 180;
	const Δλ = ((lon2 - lon1) * Math.PI) / 180;
  
	const y = Math.sin(Δλ) * Math.cos(φ2);
	const x =
	  Math.cos(φ1) * Math.sin(φ2) -
	  Math.sin(φ1) * Math.cos(φ2) * Math.cos(Δλ);
  
	const bearing = (Math.atan2(y, x) * 180) / Math.PI;
  
	return (bearing + 360) % 360; // Normalize to 0-360
  }

  // Function to handle finding nearby POIs
  async function findNearbyPOIs() {
	if (currentCoordinates) {
	  const mapData = await getMapData(options);
	  const pois = mapData.getByType("space");
  
	  // Filter POIs that have a name and calculate distances from current position to each POI
	  const distances = pois
		.filter((poi) => poi.name && poi.name.trim().length > 0 && poi.center.floorId === "m_e6c96a31fba4ef51") // Only POIs with a name
		.map((poi) => ({
		  name: poi.name,
		  distance: roundDistance(
			currentCoordinates.lat,
			currentCoordinates.lon,
			poi.center.latitude,
			poi.center.longitude
		  ),
		}));
  	  console.log(distances)

	  // Sort by distance (ascending)
	  const sortedPOIs = await distances.sort((a, b) => a.distance - b.distance);
  
	  // Take the closest 4 POIs
	  const closestPOIs = sortedPOIs.slice(0, 4).map((poi) => poi.name);
  
	  // Set the closest POIs to state
	  setNearbyPOIs(closestPOIs);
	} else {
	  console.error("Current coordinates not available.");
	}
  }

  useEffect(() => {
    init();
  }, []);

  return (
    <>
      <div ref={mapRef} id="mappedin-map" className="w-screen h-screen"></div>

      <div className="fixed bottom-4 left-4">
	  <h1>Data from JSON file</h1>
      <pre>{JSON.stringify(data.current, null, 2)}</pre>
        <button
          className="bg-blue-800 rounded text-white p-2 mt-4"
          onClick={() => {
            isPause.current = !isPause.current;
            setPaused(!paused);
          }}
        >
          {paused ? "Unpause" : "Pause"}
        </button>

        {/* Button to find nearby POIs */}
        <button
          className="bg-green-600 rounded text-white p-2 mt-4"
          onClick={findNearbyPOIs}
        >
          Where am I?
        </button>

		{nearbyPOIs.length > 0 && (
          <div className="mt-4 p-2 bg-gray-200 rounded">
            <p>Nearby Locations:</p>
            <ul>
              {nearbyPOIs.map((poi, index) => (
                <li key={index}>{poi}</li>
              ))}
            </ul>
          </div>
        )}

        {transcription && (
          <div className="mt-4 p-2 bg-gray-200 rounded">
            <p>
              <strong>{transcription}</strong>
            </p>
          </div>
        )}
      </div>
    </>
  );
};

export default Page;
