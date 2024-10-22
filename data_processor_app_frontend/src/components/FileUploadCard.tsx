import React, { useState, useRef, ChangeEvent, FormEvent } from "react";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Upload, X } from "lucide-react";
import { toast } from "sonner";

interface Metadata {
  total_rows: number;
  total_columns: number;
  null_counts: number;
  unique_counts: number;
  memory_usage: number;
  dtypes: Record<string, string>;
}

export const FileUploadCard: React.FC = () => {
  const uploadFileRef = useRef<HTMLInputElement | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [metadata, setMetadata] = useState<Metadata | null>(null);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0]);
    }
  };

  const handleSubmit = async () => {
    console.log("TEST");
    setMetadata(null);

    if (!file) {
      toast("Please upload a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post<Metadata>(
        "http://localhost:8000/process/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      setMetadata(response.data);
    } catch (err) {
      toast("There was an error processing the file.");
    }
  };

  return (
    <Card className="transform rounded-xl bg-white p-8 shadow-lg transition-all duration-300 ease-in-out hover:scale-105 dark:bg-gray-800">
      <div className="space-y-6 text-center">
        <Upload className="mx-auto h-16 w-16 text-blue-500" />
        <h2 className="text-2xl font-bold text-gray-800 dark:text-white">
          Upload Your Data File
        </h2>
        <p className="text-gray-600 dark:text-gray-300">
          Upload your CSV or Excel file and our tool will transform your data to
          a correct format
        </p>
        <input
          type="file"
          className="hidden"
          accept=".csv, .xls, .xlsx"
          onChange={handleFileChange}
          ref={uploadFileRef}
        />
        <div className="flex gap-2">
          <Button
            size="lg"
            variant="blue"
            type="button"
            onClick={() => uploadFileRef.current?.click()}
          >
            Upload File
          </Button>
          <Button
            size="lg"
            variant="main"
            onClick={() => handleSubmit()}
            disabled={!file}
          >
            Process Data
          </Button>
        </div>
        {file && (
          <div className="flex justify-start gap-2 items-center">
            <p className="text-gray-700 dark:text-gray-300">
              Selected file: <strong>{file.name}</strong>
            </p>
            <X className="hover:text-red-600" onClick={() => setFile(null)} />
          </div>
        )}
        <p className="text-sm text-gray-500 dark:text-gray-400">
          Supported formats: CSV, XLS, XLSX
        </p>
      </div>
    </Card>
  );
};
