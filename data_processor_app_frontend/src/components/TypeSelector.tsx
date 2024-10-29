import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

import { dataTypeMapping, conversionRules } from "@/utils/dataTypeMapping";

export interface TypeSelectorProps {
    value: string;
}


export const TypeSelector: React.FC<TypeSelectorProps> = ({value}) => {

const options: string[] = Array.from(new Set(Object.values(dataTypeMapping))); 

const filteredOptions = conversionRules[value];

  return (
    <Select defaultValue={value}>
      <SelectTrigger className="w-[180px]">
        <SelectValue placeholder="Select a type..." />
      </SelectTrigger>
      <SelectContent className="bg-blue-100 rounded-xl">
        {filteredOptions.map((option) => (
            <SelectItem key={option} value={option} className="bg-blue-100 hover:bg-blue-200 text-zinc-800 hover:cursor-pointer">
                {option}
            </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
};
