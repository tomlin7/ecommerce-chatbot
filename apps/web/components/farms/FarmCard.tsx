import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Farm } from "@/types";
import { MapPin, Star, Sprout, ChevronRight } from "lucide-react";
import Image from "next/image";
import Link from "next/link";

interface FarmCardProps {
  farm: Farm;
}

export function FarmCard({ farm }: FarmCardProps) {
  return (
    <Link href={`/farms/${farm.id}`}>
      <Card className="group overflow-hidden hover:shadow-lg transition-all duration-300 h-full border-green-100">
        <div className="relative aspect-video overflow-hidden">
          <Image
            src={
              farm.imageUrl || "/placeholder-farm.svg"
            }
            alt={farm.name || "Farm"}
            fill
            className="object-cover group-hover:scale-105 transition-transform duration-300"
          />
          {farm.establishedYear && (
            <Badge className="absolute top-2 left-2 bg-green-600 hover:bg-green-700">
              Est. {farm.establishedYear}
            </Badge>
          )}
        </div>

        <CardContent className="p-4 space-y-3">
          <div className="space-y-2">
            <h3 className="font-semibold text-lg group-hover:text-green-600 transition-colors">
              {farm.name}
            </h3>
            
            <div className="flex items-center text-sm text-muted-foreground">
              <MapPin className="h-4 w-4 mr-1" />
              {farm.location}
            </div>

            {farm.description && (
              <p className="text-sm text-muted-foreground line-clamp-2">
                {farm.description}
              </p>
            )}

            {/* Certifications */}
            {farm.certifications.length > 0 && (
              <div className="flex flex-wrap gap-1">
                {farm.certifications.slice(0, 3).map((cert, index) => (
                  <Badge
                    key={index}
                    variant="outline"
                    className="text-xs border-green-300 text-green-700"
                  >
                    <Sprout className="h-3 w-3 mr-1" />
                    {cert}
                  </Badge>
                ))}
                {farm.certifications.length > 3 && (
                  <Badge variant="outline" className="text-xs">
                    +{farm.certifications.length - 3} more
                  </Badge>
                )}
              </div>
            )}

            {/* Acreage */}
            {farm.acreage && (
              <div className="text-xs text-muted-foreground">
                {farm.acreage} acres
              </div>
            )}
          </div>
        </CardContent>

        <CardFooter className="p-4 pt-0">
          <Button
            variant="outline"
            className="w-full group-hover:bg-green-50 group-hover:border-green-300"
          >
            View Farm
            <ChevronRight className="ml-2 h-4 w-4" />
          </Button>
        </CardFooter>
      </Card>
    </Link>
  );
}