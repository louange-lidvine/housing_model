import React from "react";

interface Props {
    price: number | null;
    error: string | null;
}

const Result: React.FC<Props> = ({ price, error }) => {
    if (error) {
        return <div className="result error">{error}</div>;
    }
    if (price !== null) {
        return (
            <div className="result">
                Predicted Price: ${price.toLocaleString()}
            </div>
        );
    }
    return null;
};

export default Result;
