import { useState } from "react";
import { searchEvents } from "../services/eventService";

const SearchForm = () => {
  const [srcaddr, setSrcaddr] = useState("");
const [startTime, setStartTime] = useState<number | null>(null);
const [endTime, setEndTime] = useState<number | null>(null);

  const [results, setResults] = useState<any[]>([]);
  const [searchTime, setSearchTime] = useState<number | null>(null);

  const dataset_id = sessionStorage.getItem("uploadedEventdataset_id");


  const handleHomenav = () => {
    window.location.href = "/upload";
  }

  if (!dataset_id) {
    return <p className="text-red-600">Please upload an event dataset first. <span onClick={handleHomenav}>back to Upload</span></p>;
  }

const handleSearch = async () => {
  if (
    (startTime !== null && !Number.isInteger(startTime)) ||
    (endTime !== null && !Number.isInteger(endTime))
  ) {
    alert("Start Time and End Time must be integers");
    return;
  }

  if (
    startTime !== null &&
    endTime !== null &&
    startTime > endTime
  ) {
    alert("Start Time cannot be greater than End Time");
    return;
  }

  const res = await searchEvents({
    query: srcaddr,
    start_time: startTime,
    end_time: endTime,
    dataset_id,
  });

  setResults(res.results);
  setSearchTime(res.search_time_seconds);
};



  return (
    <div className="space-y-4">
      <div className="flex gap-4">
        <input
          placeholder="Source IP"
          value={srcaddr}
          onChange={(e) => setSrcaddr(e.target.value)}
          className="border p-2"
        />
       <input
  type="number"
  placeholder="Start Time"
  value={startTime ?? ""}
  onChange={(e) => {
    const value = e.target.value;
    setStartTime(value === "" ? null : Number(value));
  }}
  className="border p-2"
/>

<input
  type="number"
  placeholder="End Time"
  value={endTime ?? ""}
  onChange={(e) => {
    const value = e.target.value;
    setEndTime(value === "" ? null : Number(value));
  }}
  className="border p-2"
/>


        <button
          onClick={handleSearch}
          className="px-4 py-2 bg-green-600 text-white rounded"
        >
          Search
        </button>
      </div>

      {searchTime !== null && (
        <p className="text-sm text-gray-600">
          Search Time: {searchTime}s
        </p>
      )}

      {results.length === 0 && (<p className="text-gray-600 space-y-2 ">No results found.</p>
      )}

      <ul className="space-y-2">
        {results.map((r, idx) => (
          <div key={idx} className="border p-3 rounded bg-gray-50">
            <div className="font-medium">
              Event Found: {r.srcaddr} → {r.dstaddr} | Action: {r.action} | Log Status: {r.log_status}
            </div>
            <div className="text-sm text-gray-600">
              File: {r.file}
            </div>
          </div>
        ))}

      </ul>
    </div>
  );
};

export default SearchForm;
