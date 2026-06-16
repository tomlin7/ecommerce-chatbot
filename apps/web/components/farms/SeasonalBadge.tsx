import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

interface SeasonalBadgeProps {
  season: string;
  className?: string;
  size?: "default" | "sm" | "lg";
}

const seasonColors: Record<string, string> = {
  Spring: "bg-green-100 text-green-700 border-green-300",
  Summer: "bg-yellow-100 text-yellow-700 border-yellow-300",
  Fall: "bg-orange-100 text-orange-700 border-orange-300",
  Winter: "bg-blue-100 text-blue-700 border-blue-300",
  "Year-Round": "bg-purple-100 text-purple-700 border-purple-300",
};

export function SeasonalBadge({
  season,
  className,
  size = "default",
}: SeasonalBadgeProps) {
  const colorClass =
    seasonColors[season] || "bg-gray-100 text-gray-700 border-gray-300";

  const sizeClasses = {
    default: "px-2 py-1 text-sm",
    sm: "px-1.5 py-0.5 text-xs",
    lg: "px-3 py-1.5 text-base",
  };

  return (
    <Badge
      variant="outline"
      className={cn(
        "font-medium",
        colorClass,
        sizeClasses[size],
        className
      )}
    >
      {season}
    </Badge>
  );
}