import React, { useState } from "react";
import axios from "axios";

interface HouseData {
    Area: number;
    Bedrooms: number;
    Bathrooms: number;
    Floors: number;
    YearBuilt: number;
    Location: string;
    Condition: string;
    Garage: string;
}

interface Props {
    setPredictedPrice: (price: number | null) => void;
    setError: (error: string | null) => void;
}

const HouseForm: React.FC<Props> = ({ setPredictedPrice, setError }) => {
    const [formData, setFormData] = useState<HouseData>({
        Area: 0,
        Bedrooms: 0,
        Bathrooms: 0,
        Floors: 0,
        YearBuilt: 0,
        Location: "Downtown",
        Condition: "Excellent",
        Garage: "No",
    });

    const handleChange = (
        e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
    ) => {
        const { name, value } = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]:
                name === "Location" || name === "Condition" || name === "Garage"
                    ? value
                    : parseInt(value) || 0,
        }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        setPredictedPrice(null);

        try {
            const response = await axios.post(
                "http://127.0.0.1:8000/predict",
                formData
            );
            setPredictedPrice(response.data.predicted_price);
        } catch (err) {
            setError("Failed to predict price. Please try again.");
            console.error(err);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="house-form">
            <div className="form-group">
                <label>Area (sq ft):</label>
                <input
                    type="number"
                    name="Area"
                    value={formData.Area}
                    onChange={handleChange}
                    required
                />
            </div>
            <div className="form-group">
                <label>Bedrooms:</label>
                <input
                    type="number"
                    name="Bedrooms"
                    value={formData.Bedrooms}
                    onChange={handleChange}
                    required
                />
            </div>
            <div className="form-group">
                <label>Bathrooms:</label>
                <input
                    type="number"
                    name="Bathrooms"
                    value={formData.Bathrooms}
                    onChange={handleChange}
                    required
                />
            </div>
            <div className="form-group">
                <label>Floors:</label>
                <input
                    type="number"
                    name="Floors"
                    value={formData.Floors}
                    onChange={handleChange}
                    required
                />
            </div>
            <div className="form-group">
                <label>Year Built:</label>
                <input
                    type="number"
                    name="YearBuilt"
                    value={formData.YearBuilt}
                    onChange={handleChange}
                    required
                />
            </div>
            <div className="form-group">
                <label>Location:</label>
                <select
                    name="Location"
                    value={formData.Location}
                    onChange={handleChange}
                >
                    <option value="Downtown">Downtown</option>
                    <option value="Suburbs">Suburbs</option>
                </select>
            </div>
            <div className="form-group">
                <label>Condition:</label>
                <select
                    name="Condition"
                    value={formData.Condition}
                    onChange={handleChange}
                >
                    <option value="Excellent">Excellent</option>
                    <option value="Good">Good</option>
                    <option value="Fair">Fair</option>
                </select>
            </div>
            <div className="form-group">
                <label>Garage:</label>
                <select
                    name="Garage"
                    value={formData.Garage}
                    onChange={handleChange}
                >
                    <option value="Yes">Yes</option>
                    <option value="No">No</option>
                </select>
            </div>
            <button type="submit" className="submit-btn">
                Predict Price
            </button>
        </form>
    );
};

export default HouseForm;
