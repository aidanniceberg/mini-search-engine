import { useState } from "react";
import SearchInput from "../../components/SearchInput/SearchInput";
import styles from "./HomePage.module.css";
import { useNavigate } from "react-router-dom";

function HomePage() {
    const navigate = useNavigate();
    const [searchValue, setSearchValue] = useState("");

    const handleSubmit = () => {
        const redirect = `/search?query=${encodeURIComponent(searchValue)}`;
        navigate(redirect);
    }

    return (
        <div className={styles.wrapper}>
            <SearchInput value={searchValue} onChange={setSearchValue} onSubmit={handleSubmit} canSubmit={!!searchValue} />
        </div>
    );
}

export default HomePage;
