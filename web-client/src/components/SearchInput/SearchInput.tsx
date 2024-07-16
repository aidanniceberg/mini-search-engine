import styles from "./SearchInput.module.css";
import classNames from "classnames";
import { FormEvent } from "react";
import { GoSearch } from "react-icons/go";


export interface TextInputProps {
    value: string;
    placeholder?: string;
    canSubmit?: boolean;
    onChange: (value: string) => void;
    onSubmit: () => void;
}

export default function TextInput({ value, placeholder, canSubmit, onChange, onSubmit }: TextInputProps) {
    const submitClassNames = classNames(styles.search, {
        [styles.searchDisabled]: !canSubmit,
    });

    const handleSubmit = (event: FormEvent<HTMLButtonElement>) => {
        event.preventDefault();
        if (canSubmit) onSubmit();
    }

    return (
        <form className={styles.inputWrapper}>
            <input
                type="text"
                placeholder={placeholder}
                value={value}
                onChange={(e) => onChange(e.target.value)}
                className={styles.input}
            />
            <button type="submit" onClick={handleSubmit} className={submitClassNames}>
                <GoSearch className={styles.searchIcon} />
            </button>
        </form>
    )
}
