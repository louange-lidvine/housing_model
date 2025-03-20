import React, { useState } from "react";
import "./App.css";
import HouseForm from "../src/components/HouseForm";
import Result from "../src/components/Result";

const App: React.FC = () => {
    const [predictedPrice, setPredictedPrice] = useState<number | null>(null);
    const [error, setError] = useState<string | null>(null);

    return (
        <div className="App">
            <h1>House Price Predictor</h1>
            <HouseForm
                setPredictedPrice={setPredictedPrice}
                setError={setError}
            />
            <Result price={predictedPrice} error={error} />
        </div>
    );
};

export default App;
