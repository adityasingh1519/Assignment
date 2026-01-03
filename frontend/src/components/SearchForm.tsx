import { useState } from "react";
import { searchEvents } from "../services/eventService";

const SearchForm = () => {
  const [srcaddr, setSrcaddr] = useState("");
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");
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
    const res = await searchEvents({
      query: srcaddr ? { srcaddr } : {},
      start_time: Number(startTime),
      end_time: Number(endTime),
      dataset_id: dataset_id,
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
          placeholder="Start Time"
          value={startTime}
          onChange={(e) => setStartTime(e.target.value)}
          className="border p-2"
        />
        <input
          placeholder="End Time"
          value={endTime}
          onChange={(e) => setEndTime(e.target.value)}
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

      <ul className="space-y-2">
        {results.map((r, idx) => (
          <li key={idx} className="border p-2">
            <div>{r.event.srcaddr} → {r.event.dstaddr}</div>
            <div>Action: {r.event.action}</div>
            <div>File: {r.file}</div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SearchForm;
