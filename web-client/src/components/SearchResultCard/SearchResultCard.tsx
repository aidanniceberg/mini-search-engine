import styles from "./SearchResultCard.module.css";
import { SearchResultItem } from "../../interfaces/searchResult";
import { NavLink } from "react-router-dom";
import { useEffect, useState } from "react";


export interface SearchResultCardProps {
    item: SearchResultItem;
}

export default function SearchResultCard({ item }: SearchResultCardProps) {
    const [urlParsed, setUrlParsed] = useState<string[]>([]);

    useEffect(() => {
        const url = new URL(item.url);
        const components = url.pathname.split('/').filter(Boolean);
        const domain = url.hostname.replace(/^www\./, '');
        setUrlParsed([domain, ...components]);
    }, []);

    return (
        <div className={styles.wrapper}>
            <div>
                <NavLink to={item.url} className={styles.breadcrumbsWrapper}>
                    {urlParsed.map((c) => <span className={styles.crumb}>{c}</span>)}
                </NavLink>
            </div>
            <div>
                <NavLink to={item.url} className={styles.title}>{item.title}</NavLink>
            </div>
            <p>{item.description}</p>
        </div>
    )
}
