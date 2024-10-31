import { useState, useEffect, useRef } from "react";
import { FileUploadCard } from "@/components/FileUploadCard";
import { DataTablePreview, DataTableType } from "@/components/DataTablePreview";

function App() {
  const [data, setData] = useState<DataTableType>();

  const secondSectionRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (data && secondSectionRef.current) {
      secondSectionRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [data]);

  return (
    <div className="flex flex-col items-center justify-center bg-gradient-to-b px-40 from-blue-200 via-pink-50 to-pink-200 min-h-screen text-black">
      <main className="space-y-12 w-[85%]">
        <section className="min-h-screen flex items-center">
          <div className="grid grid-cols-1 gap-12 xl:grid-cols-2">
            <div className="space-y-6">
              <h1 className="bg-gradient-to-r from-blue-600 to-pink-600 bg-clip-text text-4xl font-extrabold tracking-tight text-transparent sm:text-5xl md:text-6xl pb-2">
                Transform Your Data into High-Quality Assets
              </h1>
              <p className="mx-auto text-xl text-gray-700 dark:text-gray-300">
                Streamline your data transformation process and unlock its full
                potential with simplicity and precision. Use our no-code
                platform to cut through the complexity and obtain
                analytics-ready datasets.
              </p>
              <p className="text-lg">Created By: Vincent Arson Taneli</p>
            </div>
            <div className="flex justify-center">
              <FileUploadCard setData={setData} />
            </div>
          </div>
        </section>
        {data && (
          <section
            ref={secondSectionRef}
            className="min-h-screen flex flex-col justify-center items-center gap-2"
          >
            <h2 className="text-blue-600 text-xl font-extrabold  sm:text-5xl md:text-6xl pb-2">
              Result
            </h2>
            <p className="mb-8">Preview of first 10 rows of the cleaned dataset</p>
            <div className="w-[90%] max-w-[90rem] h-96 overflow-auto">
              <DataTablePreview dtypes={data.dtypes} head={data.head} />
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
