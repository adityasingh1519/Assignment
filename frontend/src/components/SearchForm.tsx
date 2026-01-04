import { useState } from "react";
import { searchEvents } from "../services/eventService";

const SearchForm = () => {
  const [query, setQuery] = useState("");
  const [startTime, setStartTime] = useState<number | null>(null);
  const [endTime, setEndTime] = useState<number | null>(null);

  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any[]>([]);
  const [searchTime, setSearchTime] = useState<number | null>(null);

  const [cursor, setCursor] = useState<string | null>(null);
  const [hasMore, setHasMore] = useState(false);

  const dataset_id = sessionStorage.getItem("uploadedEventdataset_id");

  const handleHomeNav = () => {
    window.location.href = "/upload";
  };

  if (!dataset_id) {
    return (
      <p className="text-red-600">
        Please upload an event dataset first.{" "}
        <span onClick={handleHomeNav} className="underline cursor-pointer">
          Back to Upload
        </span>
      </p>
    );
  }
  const handleSearch = async () => {
    if (!query.trim() && startTime === null && endTime === null) {
      alert("Please provide at least one search criteria.");
      return;
    }

    if (
      (startTime !== null && !Number.isInteger(startTime)) ||
      (endTime !== null && !Number.isInteger(endTime))
    ) {
      alert("Start Time and End Time must be integers");
      return;
    }

    if (startTime !== null && endTime !== null && startTime > endTime) {
      alert("Start Time cannot be greater than End Time");
      return;
    }

    setLoading(true);
    setResults([]);
    setCursor(null);
    setHasMore(false);

    try {
      const res = await searchEvents({
        query,
        start_time: startTime,
        end_time: endTime,
        dataset_id,
      });

      setResults(res.results);
      setCursor(res.next_cursor);
      setHasMore(res.has_more);
      setSearchTime(res.search_time_seconds);
    } catch (error: any) {
      alert(error?.response?.data?.error || "Search failed");
    } finally {
      setLoading(false);
    }
  };

  const loadMore = async () => {
    if (!hasMore || !cursor || loading) return;

    setLoading(true);

    try {
      const res = await searchEvents({
        query,
        start_time: startTime,
        end_time: endTime,
        dataset_id,
        cursor,
      });

      setResults(prev => [...prev, ...res.results]);
      setCursor(res.next_cursor);
      setHasMore(res.has_more);
    } catch (error: any) {
      alert(error?.response?.data?.error || "Failed to load more results");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-5 gap-4">
        <input
          placeholder="account_id,instance_id, srcaddr, dstaddr, action, log_status"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="border p-2 col-span-2"
        />

        <input
          type="number"
          placeholder="Start Time"
          value={startTime ?? ""}
          onChange={(e) =>
            setStartTime(e.target.value === "" ? null : Number(e.target.value))
          }
          className="border p-2"
        />

        <input
          type="number"
          placeholder="End Time"
          value={endTime ?? ""}
          onChange={(e) =>
            setEndTime(e.target.value === "" ? null : Number(e.target.value))
          }
          className="border p-2"
        />

        <button
          onClick={handleSearch}
          disabled={loading}
          className="px-4 py-2 bg-green-600 text-white rounded disabled:opacity-50"
        >
          Search
        </button>
      </div>

      {loading && <p className="text-gray-600">Searching...</p>}

      {!loading && searchTime !== null && (
        <p className="text-sm text-gray-600">
          Search Time: {searchTime}s
        </p>
      )}

      {!loading && results.length === 0 && (
        <p className="text-gray-600">No results found.</p>
      )}

      <ul className="space-y-2">
        {results.map((r, idx) => (
          <li key={idx} className="border p-3 rounded bg-gray-50">
            <div className="font-medium">
              Event Found: {r.srcaddr} → {r.dstaddr} | Action: {r.action} | Log
              Status: {r.log_status}
            </div>
            <div className="text-sm text-gray-600">File: {r.file}</div>
          </li>
        ))}
      </ul>

      {hasMore && (
        <button
          onClick={loadMore}
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
        >
          Load more
        </button>
      )}
    </div>
  );
};

export default SearchForm;
