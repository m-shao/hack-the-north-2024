"use client";

import { useRef } from "react";
import { getMapData, show3dMap,TDirectionInstruction } from "@mappedin/mappedin-js";
import "@mappedin/mappedin-js/lib/index.css";

// See Demo API key Terms and Conditions
// https://developer.mappedin.com/v6/demo-keys-and-maps/
const options = {
	key: 'mik_Qar1NBX1qFjtljLDI52a60753',
	secret: 'mis_CXFS9WnkQkzQmy9GCt4ucn2D68zNRgVa2aiJj5hEIFM8aa40fee',
	mapId: '66ce20fdf42a3e000b1b0545'
};

const Page = () => {
	const mapRef = useRef<HTMLDivElement>(null);

	async function init() {
		const mapData = await getMapData(options);
		const mapView = await show3dMap(
			mapRef.current as HTMLDivElement,
			mapData
		);

		mapView.Labels.all();

		// Iterate through each point of interest and label it.
		for (const poi of mapData.getByType('point-of-interest')) {
			// Label the point of interest if it's on the map floor currently shown.
			if (poi.floor.id === mapView.currentFloor.id) {
				mapView.Labels.add(poi.coordinate, poi.name);
			}
		}

		// Get directions between two spaces (random)
		const startSpace = mapData.getByType("space")[10];
		const endSpace = mapData.getByType("space")[12];

		if (startSpace && endSpace) {
			const directions = mapView.getDirections(startSpace, endSpace);

			// Ensure directions are defined before proceeding
			if (directions && directions.coordinates) {
				await mapView.Paths.add(directions.coordinates, { color: "cornflowerblue" });
				directions.instructions.forEach((instruction: TDirectionInstruction) => {
					// These is the list of instructions for navigating
					console.log(`${instruction.action.type} ${instruction.action.bearing?? ''} and walk ${Math.round(instruction.distance)} meters`)
					// const markerTemplate = `
					// 	<div class="marker">
					// 		<p>${instruction.action.type} ${instruction.action.bearing ?? ''} and go ${Math.round(instruction.distance)} meters.</p>
					// 	</div>`;
				
					// mapView.Markers.add(instruction.coordinate, markerTemplate, {
					// 	rank: 2,
					// });
				});
				
				console.log("Directions:", directions);
			} else {
				console.error("Directions could not be found or are undefined.");
			}
		} else {
			console.error("Start or end space is undefined.");
		}
	}

	init();

	return (
		<>
			<div
				ref={mapRef}
				id='mappedin-map'
				className='w-screen h-screen'
			></div>
		</>
	);
};

export default Page;
