import { useEffect, useState } from "react";
import SearchInput from "../../components/SearchInput/SearchInput";
import styles from "./SearchPage.module.css";
import { useSearchParams } from "react-router-dom";
import { getResults } from "../../clients/searchClient";
import { SearchResult } from "../../interfaces/searchResult";
import SearchResultCard from "../../components/SearchResultCard/SearchResultCard";

function SearchPage() {
    const [searchParams, setSearchParams] = useSearchParams();
    const [searchValue, setSearchValue] = useState("");
    const [searchResults, setSearchResults] = useState<SearchResult | null>(null);

    const handleSubmit = () => {
        searchParams.set("query", searchValue);
        setSearchParams(searchParams);
    }

    useEffect(() => {
        const query = searchParams.get("query");
        if (query) {
            setSearchValue(query ?? "");
            getResults(query).then(setSearchResults);
        }
    }, [searchParams]);

    return (
        <div className={styles.wrapper}>
            <div className={styles.inputWrapper}>
                <SearchInput value={searchValue} onChange={setSearchValue} onSubmit={handleSubmit} canSubmit={!!searchValue} />
            </div>
            <div className={styles.resultsWrapper}>
                {searchResults && searchResults.items.map((item) => (
                    <SearchResultCard item={item} />
                ))}
            </div>
        </div>
    );
}

export default SearchPage;
