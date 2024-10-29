import React, { useState } from "react";
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableFooter,
    TableHead,
    TableHeader,
    TableRow,
  } from "@/components/ui/table"
import { dataTypeMapping } from "@/utils/dataTypeMapping";
import { TypeSelector } from "@/components/TypeSelector";

export interface DataTableType {
    dtypes: {[key: string]: string};
    head: Array<{[key: string]: any}>;
}

export const DataTablePreview: React.FC<DataTableType> = ({ dtypes, head }) => {

    return (
        <Table>
            <TableHeader>
                <TableRow className="bg-blue-300">
                    {Object.entries(dtypes).map(([column]) => (
                        <TableHead key={column} title={`Column Name: ${column}`} className="text-center">
                            <h2 className="text-lg">{column}</h2>
                        </TableHead>
                    ))}
                </TableRow>
                <TableRow className="bg-blue-200">
                    {Object.entries(dtypes).map(([column, type]) => (
                        <TableHead key={column} title={`Type: ${type}`}>
                            <TypeSelector value={dataTypeMapping[type]} />
                        </TableHead>
                    ))}
                </TableRow>
            </TableHeader>
            <TableBody>
                {head.map((row, rowIndex) => (
                    <TableRow key={rowIndex}>
                        {Object.keys(dtypes).map((column) => (
                            <TableCell key={column}>
                                {row[column]?.toString() ?? ''}
                            </TableCell>
                        ))}
                    </TableRow>
                ))}
            </TableBody>
            <TableFooter>
                <TableRow>
                    <TableCell colSpan={Object.keys(dtypes).length}>
                        Total Records: {head.length}
                    </TableCell>
                </TableRow>
            </TableFooter>
        </Table>
    );
}