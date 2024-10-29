import React, { useState, useCallback } from "react";
import axios, { AxiosError, AxiosResponse } from "axios";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Upload, X } from "lucide-react";
import { toast } from "sonner";
import { FileType, supportedFileTypes } from "@/utils/fileTypes";
import { DataTablePreview, DataTableType } from "@/components/DataTablePreview";

export interface FileUploadCardProps {
  setData: React.Dispatch<React.SetStateAction<DataTableType | undefined>>;
}

export const FileUploadCard: React.FC<FileUploadCardProps> = ({ setData }) => {
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  const validateAndSetFile = useCallback(
    (newFile: File | null) => {
      if (!newFile) {
        toast.error("No file selected");
        return;
      }

      const mimeType = newFile.type;
      if (
        !supportedFileTypes
          .map((fileType: FileType) => fileType.mimeType)
          .includes(mimeType)
      ) {
        toast.error("Unsupported File Type");
        return;
      }

      setFile(newFile);
      toast.success("File uploaded successfully");
    },
    [supportedFileTypes, setFile]
  );

  const handleDragEvent = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(e.type !== "dragleave" && e.type !== "drop");
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      handleDragEvent(e);
      const droppedFile = e.dataTransfer?.files?.[0];
      validateAndSetFile(droppedFile ?? null);
    },
    [handleDragEvent, validateAndSetFile]
  );

  const handleButtonUpload = useCallback(() => {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = supportedFileTypes.map((type) => type.mimeType).join(",");
    input.multiple = false;

    input.onchange = (e: Event) => {
      const selectedFile = (e.target as HTMLInputElement).files?.[0];
      validateAndSetFile(selectedFile ?? null);
    };

    input.click();
  }, [validateAndSetFile, supportedFileTypes]);

  const handleSubmit = async () => {
    if (!file) {
      toast.error("Please upload a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const apiURL = "http://127.0.0.1:8000";

    toast.promise(
      axios.post(`${apiURL}/api/process/`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }),
      {
        loading: "Processing data...",
        success: (response: AxiosResponse) => {
          console.log(response);
          if(response.status !== 200) {
            return "There was an error processing the file.";
          }
          setData(response.data);
          return `Data processed successfully`;
        },
        error: (err: AxiosError) => {
          return (err.response?.data as { error?: string })?.error || "There was an error processing the file.";
        },
      }
    );
  };

  return (
    <Card
      className={`
      transform rounded-xl bg-white py-8 px-16 shadow-lg transition-all duration-300 ease-in-out 
      hover:scale-105 dark:bg-gray-800
      ${isDragging ? "ring-2 ring-blue-500 bg-blue-50 dark:bg-gray-700" : ""}
    `}
    >
      <div
        className="space-y-6 text-center"
        onDragEnter={handleDragEvent}
        onDragOver={handleDragEvent}
        onDragLeave={handleDragEvent}
        onDrop={handleDrop}
      >
        <Upload
          className={`
          mx-auto h-16 w-16 
          ${isDragging ? "text-blue-600" : "text-blue-500"}
        `}
        />
        <h2 className="text-3xl font-bold text-gray-800 dark:text-white">
          Upload Your Data File
        </h2>
        <p className="text-gray-600 dark:text-gray-300">
          Drag and drop your file here, or click upload to browse
        </p>
        <div className="flex gap-2 justify-center">
          <Button
            size="lg"
            variant="blue"
            type="button"
            onClick={handleButtonUpload}
          >
            Upload File
          </Button>
          <Button
            size="lg"
            variant="main"
            disabled={!file}
            onClick={handleSubmit}
          >
            Process Data
          </Button>
        </div>
        {file && (
          <div className="flex justify-center gap-2 items-center">
            <p className="text-gray-700 dark:text-gray-300">
              Uploaded file: <strong>{file.name}</strong>
            </p>
            <X
              className="hover:text-red-600 hover:cursor-pointer"
              onClick={() => setFile(null)}
            />
          </div>
        )}
        <p className="text-sm text-gray-500 dark:text-gray-400">
          Supported formats: CSV, XLS, XLSX
        </p>
      </div>
    </Card>
  );
};

//
