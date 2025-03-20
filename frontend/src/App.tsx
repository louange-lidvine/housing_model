import React, { useState } from "react";
import "./App.css";
import HouseForm from "./components/HouseForm";
import Result from "./components/Result";

const App: React.FC = () => {
    const [predictedPrice, setPredictedPrice] = useState<number | null>(null);
    const [error, setError] = useState<string | null>(null);

    return (
        <div className="app-container">
            <div className="content-wrapper">
                {/* Left Side - House Image */}
                <div className="image-container"></div>

                {/* Right Side - Form */}
                <div className="form-container">
                    <h1>House Price Predictor</h1>
                    <HouseForm
                        setPredictedPrice={setPredictedPrice}
                        setError={setError}
                    />
                    <Result price={predictedPrice} error={error} />
                </div>
            </div>
        </div>
    );
};

export default App;
