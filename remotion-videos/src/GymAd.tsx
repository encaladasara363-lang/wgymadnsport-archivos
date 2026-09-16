import {
  AbsoluteFill,
  Sequence,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
  Easing,
} from "remotion";
import { loadFont as loadBebasNeue } from "@remotion/google-fonts/BebasNeue";
import { loadFont as loadInter } from "@remotion/google-fonts/Inter";

const { fontFamily: bebasNeue } = loadBebasNeue();
const { fontFamily: inter } = loadInter();

const RED = "#E30613";
const RED_BRIGHT = "#FF2130";
const GOLD = "#D4AF37";
const BG = "#0A0A0A";
const BG_CARD = "#141414";
const WHITE = "#FFFFFF";
const GRAY = "#CFCFCF";

const Glow: React.FC<{ delay?: number }> = ({ delay = 0 }) => {
  const frame = useCurrentFrame();
  const t = frame - delay;
  const pulse = 0.55 + 0.25 * Math.sin(t / 12);
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(circle at 50% 32%, rgba(227,6,19,${pulse * 0.35}) 0%, rgba(227,6,19,0) 55%)`,
      }}
    />
  );
};

const Bars: React.FC = () => {
  const frame = useCurrentFrame();
  const { width } = useVideoConfig();
  const bars = new Array(7).fill(0);
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      {bars.map((_, i) => {
        const speed = 6 + i * 1.3;
        const x = ((frame * speed) % (width + 400)) - 400;
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              top: `${8 + i * 12.5}%`,
              left: x,
              width: 260,
              height: 3,
              background: i % 2 === 0 ? RED : GOLD,
              opacity: 0.16,
              transform: "rotate(-8deg)",
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};

const Logo: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scale = spring({ fps, frame, config: { damping: 12, mass: 0.6 } });
  const ring = interpolate(frame, [0, 40], [0, 1], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        transform: `scale(${scale})`,
      }}
    >
      <div
        style={{
          width: 190,
          height: 190,
          borderRadius: "50%",
          border: `5px solid ${RED}`,
          boxShadow: `0 0 ${30 * ring}px rgba(227,6,19,0.65)`,
          background: `linear-gradient(160deg, ${BG_CARD}, ${BG})`,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          position: "relative",
        }}
      >
        <span
          style={{
            fontFamily: bebasNeue,
            fontSize: 108,
            color: WHITE,
            lineHeight: 1,
          }}
        >
          W
        </span>
        <div
          style={{
            position: "absolute",
            bottom: -14,
            background: GOLD,
            color: BG,
            fontFamily: bebasNeue,
            fontSize: 22,
            letterSpacing: 3,
            padding: "3px 14px",
            borderRadius: 20,
          }}
        >
          ADN
        </div>
      </div>
    </div>
  );
};

const TitleWord: React.FC<{
  text: string;
  delay: number;
  color: string;
  size: number;
}> = ({ text, delay, color, size }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const local = frame - delay;
  const y = spring({
    fps,
    frame: local,
    config: { damping: 14, mass: 0.7 },
    from: 140,
    to: 0,
  });
  const opacity = interpolate(local, [0, 12], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return (
    <div
      style={{
        fontFamily: bebasNeue,
        fontSize: size,
        color,
        letterSpacing: 4,
        lineHeight: 0.95,
        textAlign: "center",
        transform: `translateY(${y}px)`,
        opacity,
        textShadow:
          color === WHITE
            ? `0 0 40px rgba(255,255,255,0.25)`
            : `0 0 50px rgba(227,6,19,0.55)`,
      }}
    >
      {text}
    </div>
  );
};

const Tagline: React.FC = () => {
  const frame = useCurrentFrame();
  const local = frame - 55;
  const opacity = interpolate(local, [0, 20], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const y = interpolate(local, [0, 20], [16, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return (
    <div
      style={{
        fontFamily: inter,
        fontWeight: 700,
        fontSize: 34,
        color: GOLD,
        letterSpacing: 8,
        opacity,
        transform: `translateY(${y}px)`,
      }}
    >
      TOCOPILLA
    </div>
  );
};

const Divider: React.FC<{ delay: number }> = ({ delay }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const w = spring({
    fps,
    frame: frame - delay,
    config: { damping: 18 },
    from: 0,
    to: 260,
  });
  return (
    <div
      style={{
        width: w,
        height: 4,
        background: `linear-gradient(90deg, transparent, ${RED_BRIGHT}, transparent)`,
        borderRadius: 4,
      }}
    />
  );
};

const Bullet: React.FC<{ text: string; delay: number }> = ({
  text,
  delay,
}) => {
  const frame = useCurrentFrame();
  const local = frame - delay;
  const opacity = interpolate(local, [0, 14], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const x = interpolate(local, [0, 14], [-40, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: 18,
        opacity,
        transform: `translateX(${x}px)`,
      }}
    >
      <div
        style={{
          width: 14,
          height: 14,
          borderRadius: "50%",
          background: RED_BRIGHT,
          boxShadow: `0 0 16px ${RED_BRIGHT}`,
          flexShrink: 0,
        }}
      />
      <span
        style={{
          fontFamily: inter,
          fontWeight: 600,
          fontSize: 38,
          color: WHITE,
        }}
      >
        {text}
      </span>
    </div>
  );
};

const CTA: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const local = frame;
  const scale = spring({
    fps,
    frame: local,
    config: { damping: 10, mass: 0.5 },
  });
  const pulse = 1 + 0.035 * Math.sin(frame / 6);
  return (
    <div
      style={{
        transform: `scale(${scale * pulse})`,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 28,
      }}
    >
      <div
        style={{
          fontFamily: bebasNeue,
          fontSize: 100,
          color: WHITE,
          letterSpacing: 3,
          textAlign: "center",
          textShadow: `0 0 45px rgba(227,6,19,0.6)`,
        }}
      >
        ÚNETE HOY
      </div>
      <div
        style={{
          background: `linear-gradient(135deg, ${RED_BRIGHT}, ${RED})`,
          color: WHITE,
          fontFamily: bebasNeue,
          fontSize: 46,
          letterSpacing: 3,
          padding: "22px 68px",
          borderRadius: 100,
          boxShadow: `0 0 60px rgba(227,6,19,0.55)`,
        }}
      >
        RESERVA TU CUPO
      </div>
      <div
        style={{
          fontFamily: inter,
          fontWeight: 600,
          fontSize: 30,
          color: GRAY,
          letterSpacing: 2,
        }}
      >
        WGYMADNSPORT · TOCOPILLA
      </div>
    </div>
  );
};

const windowOpacity = (
  frame: number,
  inStart: number,
  inEnd: number,
  outStart: number,
  outEnd: number,
) =>
  interpolate(
    frame,
    [inStart, inEnd, outStart, outEnd],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

// Duración total: 240 frames a 30fps = 8s.
// Fase A (intro): 0-95   · Fase B (bullets): 90-170 · Fase C (CTA): 165-240
const PHASE_A = { inStart: 0, inEnd: 1, outStart: 78, outEnd: 95 };
const PHASE_B = { inStart: 90, inEnd: 105, outStart: 152, outEnd: 170 };
const PHASE_C = { inStart: 165, inEnd: 185, outStart: 999, outEnd: 999 };

export const GymAd: React.FC = () => {
  const frame = useCurrentFrame();

  const opacityA = windowOpacity(
    frame,
    PHASE_A.inStart,
    PHASE_A.inEnd,
    PHASE_A.outStart,
    PHASE_A.outEnd,
  );
  const opacityB = windowOpacity(
    frame,
    PHASE_B.inStart,
    PHASE_B.inEnd,
    PHASE_B.outStart,
    PHASE_B.outEnd,
  );
  const opacityC = interpolate(frame, [PHASE_C.inStart, PHASE_C.inEnd], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ background: BG }}>
      <AbsoluteFill
        style={{
          background: `linear-gradient(180deg, ${BG} 0%, ${BG_CARD} 55%, ${BG} 100%)`,
        }}
      />
      <Bars />
      <Glow />

      <Sequence from={PHASE_A.inStart} durationInFrames={PHASE_A.outEnd}>
        <AbsoluteFill
          style={{
            opacity: opacityA,
            justifyContent: "center",
            alignItems: "center",
            gap: 26,
            padding: "0 60px",
          }}
        >
          <Logo />
          <div style={{ height: 8 }} />
          <TitleWord text="WGYM" delay={18} color={WHITE} size={150} />
          <TitleWord text="ADNSPORT" delay={30} color={RED_BRIGHT} size={150} />
          <Tagline />
        </AbsoluteFill>
      </Sequence>

      <Sequence
        from={PHASE_B.inStart}
        durationInFrames={PHASE_B.outEnd - PHASE_B.inStart}
      >
        <AbsoluteFill
          style={{
            opacity: opacityB,
            justifyContent: "center",
            alignItems: "center",
            gap: 30,
          }}
        >
          <Divider delay={0} />
          <div style={{ display: "flex", flexDirection: "column", gap: 26 }}>
            <Bullet text="MUSCULACIÓN" delay={6} />
            <Bullet text="FUNCIONAL & HIIT" delay={14} />
            <Bullet text="ASESORÍA PERSONALIZADA" delay={22} />
          </div>
        </AbsoluteFill>
      </Sequence>

      <Sequence from={PHASE_C.inStart}>
        <AbsoluteFill
          style={{
            opacity: opacityC,
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <CTA />
        </AbsoluteFill>
      </Sequence>
    </AbsoluteFill>
  );
};
