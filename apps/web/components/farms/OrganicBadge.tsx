import { Badge } from "@/components/ui/badge";
import { Sprout, CheckCircle } from "lucide-react";
import { cn } from "@/lib/utils";

interface OrganicBadgeProps {
  certified?: boolean;
  className?: string;
  showLabel?: boolean;
  size?: "default" | "sm" | "lg";
}

export function OrganicBadge({
  certified = true,
  className,
  showLabel = true,
  size = "default",
}: OrganicBadgeProps) {
  if (!certified) return null;

  const sizeClasses = {
    default: "px-2 py-1 text-sm",
    sm: "px-1.5 py-0.5 text-xs",
    lg: "px-3 py-1.5 text-base",
  };

  return (
    <Badge
      className={cn(
        "bg-green-600 hover:bg-green-700 text-white font-medium",
        sizeClasses[size],
        className
      )}
    >
      <Sprout className={cn("mr-1", size === "sm" ? "h-3 w-3" : "h-4 w-4")} />
      {showLabel && "Organic Certified"}
    </Badge>
  );
}

interface CertificationBadgeProps {
  certification: string;
  className?: string;
}

export function CertificationBadge({
  certification,
  className,
}: CertificationBadgeProps) {
  return (
    <Badge
      variant="outline"
      className={cn(
        "border-green-300 text-green-700 bg-green-50 font-medium",
        className
      )}
    >
      <CheckCircle className="h-3 w-3 mr-1" />
      {certification}
    </Badge>
  );
}