import { ChangeEvent, MouseEvent, FC, useState } from "react";

import TextFever from "./types/TextFever";
import { CircularProgress } from "@mui/material";

import logo from "./logo.png";
import style from "./App.module.scss";
import axios from "axios";

const App: FC = () => {
    const [isProgress, setIsProgress] = useState<boolean>(false);
    const [text, setText] = useState<string>("");
    const [result, setResult] = useState<TextFever>();

    const handleOnChange = (e: ChangeEvent<HTMLInputElement>) => {
        setText(e.currentTarget.value);
    }

    const handleOnClick = (e: MouseEvent<HTMLInputElement>) => {
        getTextFeverAsync();
    }

    const getTextFeverAsync = async () => {
        setIsProgress(true);

        await axios.post(
            "https://77ba-59-132-68-231.ngrok-free.app/getTextFervor",
            {"text": text},
            {
                headers: {
                    "ngrok-skip-browser-warning": "true",
                    "Content-Type": "application/json",
                },
                withCredentials: true
            }
        )
            .then((res) => {
                setResult(res.data);
            })
            .catch(() => {
                console.log("えらーやねん")
            });

        setIsProgress(false);
    }

    return (
        <div className={style.container}>
            <img src={logo} alt="logo"/>
            <input
                type="text"
                value={text}
                onChange={handleOnChange}
                placeholder="ここに熱血ワードを入力"
            />
            <p>🔥 {text} 🔥</p>
            <input
                type="button"
                value="熱血度を測定"
                onClick={handleOnClick}
            />
            {isProgress &&
                <div>
                    <p>🔥 熱血採点中 🔥</p>
                    <CircularProgress/>
                </div>
            }
            {result != null &&
                <div>
                    <p>採点結果</p>
                    <p>熱血度: {result.value} 🔥</p>
                    <p>理由: {result.reason}</p>
                </div>
            }
        </div>
    );
}

export default App;