import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { Sprout, Sun, Leaf, Snowflake, ChevronRight } from "lucide-react";

interface SeasonalItem {
  name: string;
  months: number[]; // 0-11 (Jan-Dec)
  peakMonths: number[];
  category?: string;
}

interface SeasonalCalendarProps {
  items?: SeasonalItem[];
  currentMonth?: number;
  className?: string;
}

const seasonIcons = {
  Spring: Sprout,
  Summer: Sun,
  Fall: Leaf,
  Winter: Snowflake,
};

const monthNames = [
  "Янв", "Фев", "Мар", "Апр", "Май", "Июн",
  "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"
];

const seasons = [
  { name: "Spring", months: [2, 3, 4] },
  { name: "Summer", months: [5, 6, 7] },
  { name: "Fall", months: [8, 9, 10] },
  { name: "Winter", months: [11, 0, 1] },
];

const defaultSeasonalItems: SeasonalItem[] = [
  { name: "Strawberries", months: [4, 5, 6], peakMonths: [5, 6], category: "Berries" },
  { name: "Tomatoes", months: [5, 6, 7, 8], peakMonths: [6, 7], category: "Vegetables" },
  { name: "Corn", months: [6, 7, 8], peakMonths: [7, 8], category: "Vegetables" },
  { name: "Apples", months: [7, 8, 9, 10], peakMonths: [8, 9], category: "Fruits" },
  { name: "Squash", months: [8, 9, 10, 11], peakMonths: [9, 10], category: "Vegetables" },
  { name: "Leafy Greens", months: [2, 3, 4, 8, 9, 10], peakMonths: [3, 9], category: "Greens" },
];

export function SeasonalCalendar({
  items = defaultSeasonalItems,
  currentMonth: propMonth,
  className,
}: SeasonalCalendarProps) {
  const currentMonth = propMonth ?? new Date().getMonth();

  const getCurrentSeason = () => {
    return seasons.find(s => s.months.includes(currentMonth));
  };

  const getItemsForMonth = (month: number) => {
    return items.filter(item => item.months.includes(month));
  };

  const getPeakItemsForMonth = (month: number) => {
    return items.filter(item => item.peakMonths.includes(month));
  };

  const currentSeason = getCurrentSeason();
  const SeasonIcon = currentSeason ? seasonIcons[currentSeason.name as keyof typeof seasonIcons] : null;

  return (
    <Card className={cn("border-green-100", className)}>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>Сезонный календарь</span>
          {currentSeason && SeasonIcon && (
            <div className="flex items-center gap-2">
              <SeasonIcon className="h-5 w-5 text-green-600" />
              <span className="text-sm font-normal text-muted-foreground">
                {currentSeason.name}
              </span>
            </div>
          )}
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Month Selector */}
        <div className="grid grid-cols-6 gap-2">
          {monthNames.map((month, index) => {
            const isCurrentMonth = index === currentMonth;
            const hasItems = getItemsForMonth(index).length > 0;
            return (
              <button
                key={month}
                className={cn(
                  "text-xs py-2 px-1 rounded-md transition-colors",
                  isCurrentMonth
                    ? "bg-green-600 text-white font-medium"
                    : hasItems
                    ? "bg-green-50 text-green-700 hover:bg-green-100"
                    : "text-muted-foreground hover:bg-muted"
                )}
              >
                {month}
              </button>
            );
          })}
        </div>

        {/* Current Month Items */}
        <div className="space-y-3">
          <h4 className="text-sm font-medium text-muted-foreground">
            Доступно в этом месяце
          </h4>
          <div className="grid grid-cols-2 gap-3">
            {getItemsForMonth(currentMonth).map((item) => (
              <div
                key={item.name}
                className="flex items-center justify-between p-3 rounded-lg border bg-card hover:border-green-300 transition-colors cursor-pointer"
              >
                <div className="space-y-1">
                  <div className="font-medium text-sm">{item.name}</div>
                  {item.category && (
                    <div className="text-xs text-muted-foreground">
                      {item.category}
                    </div>
                  )}
                </div>
                {item.peakMonths.includes(currentMonth) && (
                  <Badge className="bg-green-100 text-green-700 text-xs">
                    Пик
                  </Badge>
                )}
              </div>
            ))}
            {getItemsForMonth(currentMonth).length === 0 && (
              <div className="col-span-2 text-sm text-muted-foreground text-center py-4">
                Нет сезонных товаров в этом месяце
              </div>
            )}
          </div>
        </div>

        {/* Peak Season Highlights */}
        {getPeakItemsForMonth(currentMonth).length > 0 && (
          <div className="space-y-3">
            <h4 className="text-sm font-medium text-green-600 flex items-center gap-2">
              <Sprout className="h-4 w-4" />
              На пике свежести
            </h4>
            <div className="flex flex-wrap gap-2">
              {getPeakItemsForMonth(currentMonth).map((item) => (
                <Badge
                  key={item.name}
                  variant="outline"
                  className="border-green-300 text-green-700 bg-green-50"
                >
                  {item.name}
                </Badge>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

interface SeasonalMonthViewProps {
  month: number;
  items?: SeasonalItem[];
  className?: string;
}

export function SeasonalMonthView({
  month,
  items = defaultSeasonalItems,
  className,
}: SeasonalMonthViewProps) {
  const currentItems = items.filter(item => item.months.includes(month));
  const peakItems = items.filter(item => item.peakMonths.includes(month));

  return (
    <Card className={cn("border-green-100", className)}>
      <CardHeader>
        <CardTitle className="text-xl">
          Урожай — {monthNames[month]}
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {currentItems.length === 0 ? (
          <p className="text-muted-foreground text-center py-4">
            Нет сезонных продуктов в {monthNames[month]}
          </p>
        ) : (
          <div className="space-y-3">
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {currentItems.map((item) => (
                <div
                  key={item.name}
                  className="p-3 rounded-lg border bg-card hover:border-green-300 transition-colors"
                >
                  <div className="font-medium text-sm">{item.name}</div>
                  {item.category && (
                    <div className="text-xs text-muted-foreground mt-1">
                      {item.category}
                    </div>
                  )}
                  {peakItems.includes(item) && (
                    <Badge className="mt-2 bg-green-100 text-green-700 text-xs">
                      Пик сезона
                    </Badge>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}