"use client";

import { useRef, useReducer } from "react";

import { getMapData, show3dMap } from "@mappedin/mappedin-js";
import "@mappedin/mappedin-js/lib/index.css";

// See Demo API key Terms and Conditions
// https://developer.mappedin.com/v6/demo-keys-and-maps/
const options = {
	key: "mik_yeBk0Vf0nNJtpesfu560e07e5",
	secret: "mis_2g9ST8ZcSFb5R9fPnsvYhrX3RyRwPtDGbMGweCYKEq385431022",
	mapId: "65c0ff7430b94e3fabd5bb8c",
};

const Page = () => {
	const mapRef = useRef<HTMLDivElement>(null);

	async function init() {
		const mapData = await getMapData(options);
		const mapView = await show3dMap(
			mapRef.current as HTMLDivElement,
			mapData
		);

		const directions = mapView.getDirections(
			mapData.getByType("space")[0],
			mapData.getByType("space")[5]
		);

		console.log(directions);
	}

	init();

	return (
		<>
			<div
				ref={mapRef}
				id='mappedin-map'
				className='w-screen h-screen'
			></div>
			;
		</>
	);
};

export default Page;
