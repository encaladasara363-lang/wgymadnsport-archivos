import { Composition } from "remotion";
import { GymAd } from "./GymAd";

export const MyComposition = () => {
  return (
    <Composition
      id="GymAd"
      component={GymAd}
      durationInFrames={240}
      fps={30}
      width={1080}
      height={1920}
    />
  );
};
