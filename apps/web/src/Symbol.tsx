import type { Collection } from "@quantic/power";
export function Symbol({ kind }: { kind: Collection }) {
  return (
    <svg
      width="44"
      height="28"
      viewBox="0 0 44 28"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.7"
      aria-hidden="true"
    >
      {kind === "buses" ? (
        <path d="M3 14H41M22 3V25" />
      ) : kind === "loads" ? (
        <path d="M22 2V9M12 10H32L22 25Z" />
      ) : kind === "generators" ? (
        <>
          <circle cx="22" cy="14" r="11" />
          <text
            x="22"
            y="19"
            textAnchor="middle"
            stroke="none"
            fill="currentColor"
            fontSize="13"
          >
            G
          </text>
        </>
      ) : kind === "external_grids" ? (
        <>
          <path d="M8 23L22 3L36 23M13 16H31M18 9H26M12 23H32" />
        </>
      ) : kind === "shunts" ? (
        <path d="M22 2V9M9 10H35M9 15H35M22 16V26" />
      ) : kind === "transformers" ? (
        <>
          <circle cx="17" cy="14" r="9" />
          <circle cx="27" cy="14" r="9" />
        </>
      ) : (
        <path d="M2 14H42" />
      )}
    </svg>
  );
}
