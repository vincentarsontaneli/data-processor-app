import { useState } from "react";
import { FileUploadCard } from "@/components/FileUploadCard";

interface Metadata {
  total_rows: number;
  total_columns: number;
  null_counts: number;
  unique_counts: number;
  memory_usage: number;
  dtypes: Record<string, string>;
}


function App() {

  const [metadata, setMetadata] = useState<Metadata | null>(null);

  return (
    <div className="flex flex-col items-center justify-center bg-gradient-to-b from-blue-200 via-pink-50 to-pink-200 h-full min-h-screen text-black">
      <main className="px-40">
        <section className="px-4 py-12 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 gap-12 lg:grid-cols-2">
            <div className="space-y-6">
              <h1 className="bg-gradient-to-r from-blue-600 to-pink-600 bg-clip-text text-4xl font-extrabold tracking-tight text-transparent sm:text-5xl md:text-6xl pb-2">
                Transform Your Data into High-Quality Assets
              </h1>
              <p className="mx-auto text-xl text-gray-700 dark:text-gray-300">
                Streamline your data transformation process and unlock its full
                potential with simplicity and precision. Use our no-code platform to cut through the complexity and obtain analytics-ready datasets.
              </p>
              <p className="text-lg">Created By: Vincent Arson Taneli</p>
            </div>
            <div className="flex justify-center">
              <FileUploadCard />
            </div>
          </div>
        </section>
      </main>
      
    </div>
  );
}

export default App;
