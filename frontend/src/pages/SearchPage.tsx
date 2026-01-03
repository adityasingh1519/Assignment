import SearchForm from "../components/SearchForm";

const SearchPage = () => {
  return (
    <div className="p-6 max-w-5xl mx-auto">
      <h1 className="text-xl font-semibold mb-4">Search Events</h1>
      <SearchForm />
    </div>
  );
};

export default SearchPage;
