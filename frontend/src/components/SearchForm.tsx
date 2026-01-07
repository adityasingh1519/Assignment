import { useState } from "react";
import { searchEvents } from "../services/eventService";

const SearchForm = () => {
  const [query, setQuery] = useState("");
  const [startTime, setStartTime] = useState<number | null>(null);
  const [endTime, setEndTime] = useState<number | null>(null);

  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any[]>([]);
  const [searchTime, setSearchTime] = useState<number | null>(null);

  const [currentPage, setCurrentPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [hasMore, setHasMore] = useState(false);
  const limit = 50;

  const dataset_id = sessionStorage.getItem("uploadedEventdataset_id");

  const handleHomeNav = () => {
    window.location.href = "/upload";
  };

  if (!dataset_id) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center p-4">
        <div className="bg-slate-800 rounded-xl p-8 shadow-2xl border border-red-500/50 max-w-md">
          <div className="flex items-center space-x-3 mb-4">
            <svg
              className="h-8 w-8 text-red-500"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
            <h3 className="text-xl font-bold text-red-400">No Dataset Found</h3>
          </div>
          <p className="text-slate-300 mb-6">
            Please upload an event dataset first to start searching.
          </p>
          <button
            onClick={handleHomeNav}
            className="w-full px-4 py-3 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white font-semibold rounded-lg transition-all duration-200"
          >
            Go to Upload
          </button>
        </div>
      </div>
    );
  }

  const handleSearch = async (page = 1) => {
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
    if (page === 1) {
      setResults([]);
    }

    try {
      const res = await searchEvents({
        query,
        start_time: startTime,
        end_time: endTime,
        dataset_id,
        page,
        limit,
      });

      setResults(res.results);
      setTotalCount(res.total_count);
      setHasMore(res.has_more);
      setCurrentPage(page);
      setSearchTime(res.search_time_seconds);
    } catch (error: any) {
      alert(error?.response?.data?.error || "Search failed");
    } finally {
      setLoading(false);
    }
  };

  const totalPages = Math.ceil(totalCount / limit);

  const handlePageChange = (page: number) => {
    handleSearch(page);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400 mb-2">
            Event Search
          </h1>
        </div>

        {/* Search Form */}
        <div className="bg-slate-800 rounded-xl shadow-2xl p-6 border border-slate-700 mb-6">
          <div className="grid grid-cols-1 lg:grid-cols-5 gap-4 mb-4">
            <div className="lg:col-span-2">
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Search Query
              </label>
              <input
                placeholder="account_id, instance_id, srcaddr, dstaddr..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="w-full px-4 py-3 bg-slate-900 border border-slate-600 rounded-lg text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Start Time
              </label>
              <input
                type="number"
                placeholder="Unix timestamp"
                value={startTime ?? ""}
                onChange={(e) =>
                  setStartTime(e.target.value === "" ? null : Number(e.target.value))
                }
                className="w-full px-4 py-3 bg-slate-900 border border-slate-600 rounded-lg text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                End Time
              </label>
              <input
                type="number"
                placeholder="Unix timestamp"
                value={endTime ?? ""}
                onChange={(e) =>
                  setEndTime(e.target.value === "" ? null : Number(e.target.value))
                }
                className="w-full px-4 py-3 bg-slate-900 border border-slate-600 rounded-lg text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
              />
            </div>

            <div className="flex items-end">
              <button
                onClick={() => handleSearch(1)}
                disabled={loading}
                className="w-full px-6 py-3 bg-blue-600  text-white font-semibold rounded-lg shadow-lg  disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
              >
                {loading ? (
                  <span className="flex items-center justify-center">
                    <svg
                      className="animate-spin h-5 w-5 text-white"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                    >
                      <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                      ></circle>
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                      ></path>
                    </svg>
                  </span>
                ) : (
                  "Search"
                )}
              </button>
            </div>
          </div>

          {/* Search Stats */}
          {!loading && searchTime !== null && (
            <div className="flex items-center justify-between pt-4 border-t border-slate-700">
              <div className="flex items-center space-x-6">
                <div className="flex items-center space-x-2">
                  <svg
                    className="h-5 w-5 text-blue-400"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                    />
                  </svg>
                  <span className="text-slate-300 text-sm font-medium">
                    {totalCount.toLocaleString()} results
                  </span>
                </div>
                <div className="flex items-center space-x-2">
                  <svg
                    className="h-5 w-5 text-cyan-400"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  <span className="text-slate-300 text-sm font-medium">
                    {searchTime.toFixed(4)}s
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Results */}
        {loading && (
          <div className="flex justify-center items-center py-12">
            <div className="text-center">
              <svg
                className="animate-spin h-12 w-12 text-blue-500 mx-auto mb-4"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              <p className="text-slate-400">Searching events...</p>
            </div>
          </div>
        )}

        {!loading && results.length === 0 && searchTime !== null && (
          <div className="bg-slate-800 rounded-xl p-12 text-center border border-slate-700">
            <svg
              className="h-16 w-16 text-slate-600 mx-auto mb-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <p className="text-slate-400 text-lg">No results found</p>
            <p className="text-slate-500 text-sm mt-2">
              Try adjusting your search criteria
            </p>
          </div>
        )}

      {!loading && results.length > 0 && (
  <div className="space-y-1">
    {results.map((r, idx) => (
      <div
        key={idx}
        className="bg-slate-800 rounded-lg p-3 border border-slate-700 "
      >
        {/* Top section */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <span className="text-white text-xs font-medium uppercase tracking-wide">
              Event Found 
            </span>
            <p className="text-blue-400 font-mono text-sm mt-1">
              {r.srcaddr} - {r.dstaddr}
            </p>
          </div>


          <div>
            <span className="text-white text-xs font-medium uppercase tracking-wide">
              Action
            </span>
            <p
              className={`font-semibold text-sm mt-1 ${
                r.action === "ACCEPT"
                  ? "text-green-400"
                  : r.action === "REJECT"
                  ? "text-red-400"
                  : "text-yellow-400"
              }`}
            >
              {r.action}
            </p>
          </div>

          <div>
            <span className="text-white text-xs font-medium uppercase tracking-wide">Status</span>
            <p className="text-slate-300 font-mono text-sm mt-1">
              {r.log_status}
            </p>
          </div>

          <div>
            <span className="text-white text-xs font-medium uppercase tracking-wide">Source File:</span>
            <p className="text-slate-300 font-mono text-sm mt-1">
             {r.source_file_name}
            </p>
          </div>

        </div>
      </div>
    ))}
  </div>
)}


        {/* Pagination */}
        {!loading && results.length > 0 && totalPages > 1 && (
          <div className="mt-8 flex items-center justify-between bg-slate-800 rounded-xl p-4 border border-slate-700">
            <div className="text-slate-400 text-sm">
              Page {currentPage} of {totalPages}
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => handlePageChange(currentPage - 1)}
                disabled={currentPage === 1 || loading}
                className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-slate-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                Previous
              </button>
              
              {/* Page Numbers */}
              <div className="hidden md:flex space-x-2">
                {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                  let pageNum;
                  if (totalPages <= 5) {
                    pageNum = i + 1;
                  } else if (currentPage <= 3) {
                    pageNum = i + 1;
                  } else if (currentPage >= totalPages - 2) {
                    pageNum = totalPages - 4 + i;
                  } else {
                    pageNum = currentPage - 2 + i;
                  }
                  
                  return (
                    <button
                      key={pageNum}
                      onClick={() => handlePageChange(pageNum)}
                      disabled={loading}
                      className={`px-4 py-2 rounded-lg transition-all ${
                        currentPage === pageNum
                          ? "bg-blue-600 text-white"
                          : "bg-slate-700 hover:bg-slate-600 text-slate-300"
                      } disabled:opacity-50 disabled:cursor-not-allowed`}
                    >
                      {pageNum}
                    </button>
                  );
                })}
              </div>

              <button
                onClick={() => handlePageChange(currentPage + 1)}
                disabled={!hasMore || loading}
                className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-slate-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                Next
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SearchForm;