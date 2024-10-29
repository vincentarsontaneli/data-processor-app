export type FileType = {
    extension: string;
    mimeType: string;
}
export const supportedFileTypes = [
    { "extension": ".csv", "mimeType": "application/csv" },
    { "extension": ".csv", "mimeType": "text/csv" },
    { "extension": ".xls", "mimeType": "application/vnd.ms-excel" },
    { "extension": ".xlsx", "mimeType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" }
];