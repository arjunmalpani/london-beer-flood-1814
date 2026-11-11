import React from "react";
import { Composition } from "remotion";
import { BeerFloodShort, BEER_FLOOD_FRAMES } from "./videos/beer_flood/BeerFlood";

export const Root: React.FC = () => {
  return (
    <>
      <Composition
        id="BeerFlood"
        component={BeerFloodShort}
        durationInFrames={BEER_FLOOD_FRAMES}
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
