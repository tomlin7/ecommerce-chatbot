import { Calendar, Clock, MapPin } from "lucide-react";
import { cn } from "@/lib/utils";

interface HarvestInfoProps {
  harvestDate?: string;
  farmLocation?: string;
  className?: string;
  showIcon?: boolean;
  compact?: boolean;
}

export function HarvestInfo({
  harvestDate,
  farmLocation,
  className,
  showIcon = true,
  compact = false,
}: HarvestInfoProps) {
  if (!harvestDate && !farmLocation) return null;

  const formatHarvestDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return "Сегодня";
    if (diffDays === 1) return "Вчера";
    if (diffDays <= 7) return `${diffDays} дн. назад`;

    return date.toLocaleDateString("ru-RU", {
      month: "short",
      day: "numeric",
    });
  };

  const getFreshnessLevel = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays <= 2) return { level: "peak", label: "Максимальная свежесть", color: "text-green-600" };
    if (diffDays <= 5) return { level: "fresh", label: "Очень свежий", color: "text-green-500" };
    if (diffDays <= 10) return { level: "good", label: "Свежий", color: "text-yellow-600" };
    return { level: "ok", label: "Хороший", color: "text-orange-600" };
  };

  const freshness = harvestDate ? getFreshnessLevel(harvestDate) : null;

  return (
    <div className={cn("space-y-1", className)}>
      {harvestDate && (
        <div className={cn("flex items-center", compact ? "text-xs" : "text-sm")}>
          {showIcon && (
            <Calendar className={cn("mr-1.5", compact ? "h-3 w-3" : "h-4 w-4")} />
          )}
          <span className="text-muted-foreground">Собрано: </span>
          <span className={cn("ml-1 font-medium", freshness?.color)}>
            {formatHarvestDate(harvestDate)}
          </span>
          {freshness && !compact && (
            <span className={cn("ml-2 text-xs", freshness.color)}>
              • {freshness.label}
            </span>
          )}
        </div>
      )}

      {farmLocation && (
        <div className={cn("flex items-center", compact ? "text-xs" : "text-sm")}>
          {showIcon && (
            <MapPin className={cn("mr-1.5", compact ? "h-3 w-3" : "h-4 w-4")} />
          )}
          <span className="text-muted-foreground">{farmLocation}</span>
        </div>
      )}
    </div>
  );
}

interface FreshnessIndicatorProps {
  harvestDate: string;
  className?: string;
}

export function FreshnessIndicator({ harvestDate, className }: FreshnessIndicatorProps) {
  const freshness = getFreshnessData(harvestDate);

  return (
    <div className={cn("flex items-center gap-2", className)}>
      <div className="flex items-center gap-1">
        <Clock className="h-4 w-4 text-muted-foreground" />
        <span className={cn("font-medium", freshness.color)}>{freshness.label}</span>
      </div>
      <div className="flex gap-1">
        {[1, 2, 3, 4, 5].map((level) => (
          <div
            key={level}
            className={cn(
              "h-2 w-6 rounded-full",
              level <= freshness.score
                ? freshness.bgColor
                : "bg-gray-200"
            )}
          />
        ))}
      </div>
    </div>
  );
}

function getFreshnessData(dateString: string) {
  const date = new Date(dateString);
  const now = new Date();
  const diffTime = Math.abs(now.getTime() - date.getTime());
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

  if (diffDays <= 2) {
    return { score: 5, label: "Максимальная свежесть", color: "text-green-600", bgColor: "bg-green-500" };
  }
  if (diffDays <= 5) {
    return { score: 4, label: "Очень свежий", color: "text-green-500", bgColor: "bg-green-400" };
  }
  if (diffDays <= 10) {
    return { score: 3, label: "Свежий", color: "text-yellow-600", bgColor: "bg-yellow-500" };
  }
  if (diffDays <= 15) {
    return { score: 2, label: "Хороший", color: "text-orange-600", bgColor: "bg-orange-500" };
  }
  return { score: 1, label: "Приемлемый", color: "text-red-600", bgColor: "bg-red-500" };
}