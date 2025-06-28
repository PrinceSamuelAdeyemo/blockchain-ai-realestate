"use client";
import { useState } from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { apiUrl } from "@/utils/env";

const initialState = {
  title: "",
  slug: "",
  address: "",
  city: "",
  state: "",
  country: "",
  postal_code: "",
  total_area: "",
  usable_area: "",
  bedrooms: "",
  bathrooms: "",
  building_age: "",
  total_floors: "",
  floor_number: "",
  country_encoded: "",
  price_per_sqm: "",
  base_value: "",
  year_built: "",
  description: "",
  property_type: "",
  owners: "",
};


const requiredFields = [
  "title",
  "slug",
  "address",
  "city",
  "state",
  "country",
  "postal_code",
  "total_area",
  "usable_area",
  "bedrooms",
  "bathrooms",
  "building_age",
  "total_floors",
  "floor_number",
  "country_encoded",
  "price_per_sqm",
  "base_value",
  "year_built",
  "description",
  "property_type",
  "owners",
];


export default function ListPropertyPage() {
  const [form, setForm] = useState(initialState);
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const isComplete = requiredFields.every((f) => form[f as keyof typeof form]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    setSuccess(null);
    try {
      const res = await fetch(`${apiUrl}/property/api/v1/properties/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...form,
          total_area: parseFloat(form.total_area),
          usable_area: parseFloat(form.usable_area),
          bedrooms: parseInt(form.bedrooms),
          bathrooms: parseInt(form.bathrooms),
          building_age: parseInt(form.building_age),
          total_floors: parseInt(form.total_floors),
          floor_number: parseInt(form.floor_number),
          country_encoded: parseInt(form.country_encoded),
          price_per_sqm: parseFloat(form.price_per_sqm),
          base_value: parseFloat(form.base_value),
          owners: form.owners.split(",").map((id) => id.trim()),
        }),
      });
      if (!res.ok) throw new Error("Failed to create property");
      setSuccess("Property listed successfully!");
      setForm(initialState);
    } catch (err: any) {
      setError(err.message || "Error submitting property");
    }
    setSubmitting(false);
  };

  return (
    <div>
      <Navbar />
      <div className="max-w-2xl mx-auto mt-10 p-8 bg-white rounded-xl shadow-lg">
        <h1 className="text-2xl font-bold mb-6 text-center text-blue-700">List a New Property</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
    <input
      className="input input-bordered"
      name="title"
      placeholder="Title*"
      value={form.title}
      onChange={handleChange}
      required
    />
    <input
      className="input input-bordered"
      name="slug"
      placeholder="Slug*"
      value={form.slug}
      onChange={handleChange}
      required
    />
    <input
      className="input input-bordered"
      name="address"
      placeholder="Address*"
      value={form.address}
      onChange={handleChange}
      required
    />
    <input
      className="input input-bordered"
      name="city"
      placeholder="City*"
      value={form.city}
      onChange={handleChange}
      required
    />
    <input
      className="input input-bordered"
      name="state"
      placeholder="State*"
      value={form.state}
      onChange={handleChange}
      required
    />
    <input
      className="input input-bordered"
      name="country"
      placeholder="Country*"
      value={form.country}
      onChange={handleChange}
      required
    />
    <input
      className="input input-bordered"
      name="postal_code"
      placeholder="Postal Code*"
      value={form.postal_code}
      onChange={handleChange}
      required
    />
    <input
      className="input input-bordered"
      name="total_area"
      placeholder="Total Area (m²)*"
      type="number"
      value={form.total_area}
      onChange={handleChange}
      required
    />
    <input
      className="input input-bordered"
      name="usable_area"
      placeholder="Usable Area (m²)*"
      type="number"
      value={form.usable_area}
      onChange={handleChange}
      required
    />
    <input
      className="input input-bordered"
      name="bedrooms"
      placeholder="Bedrooms*"
      type="number"
      value={form.bedrooms}
      onChange={handleChange}
      required
    />
    <input
      className="input input-bordered"
      name="bathrooms"
      placeholder="Bathrooms*"
      type="number"
      value={form.bathrooms}
      onChange={handleChange}
      required
    />
    <input
      className="input input-bordered"
      name="building_age"
      placeholder="Building Age*"
      type="number"
      value={form.building_age}
      onChange={handleChange}
      required
    />
    <input
      className="input input-bordered"
      name="total_floors"
      placeholder="Total Floors*"
      type="number"
      value={form.total_floors}
      onChange={handleChange}
      required
    />
    <input
      className="input input-bordered"
      name="floor_number"
      placeholder="Apartment Floor*"
      type="number"
      value={form.floor_number}
      onChange={handleChange}
      required
    />
    <input
      className="input input-bordered"
      name="country_encoded"
      placeholder="Country Encoded*"
      type="number"
      value={form.country_encoded}
      onChange={handleChange}
      required
    />
    <input
      className="input input-bordered"
      name="price_per_sqm"
      placeholder="Price per sqm*"
      type="number"
      value={form.price_per_sqm}
      onChange={handleChange}
      required
    />
    <input
      className="input input-bordered"
      name="base_value"
      placeholder="Base Value (USD)*"
      type="number"
      value={form.base_value}
      onChange={handleChange}
      required
    />
    <input
      className="input input-bordered"
      name="year_built"
      placeholder="Year Built*"
      type="number"
      value={form.year_built}
      onChange={handleChange}
      required
    />
    <input
      className="input input-bordered"
      name="description"
      placeholder="Description*"
      value={form.description}
      onChange={handleChange}
      required
    />
    <input
      className="input input-bordered"
      name="property_type"
      placeholder="Property Type (ID or Name)*"
      value={form.property_type}
      onChange={handleChange}
      required
    />
    <input
      className="input input-bordered"
      name="owners"
      placeholder="Owner(s) (User ID, comma separated)*"
      value={[form.owners]}
      onChange={handleChange}
      required
    />
  </div>




          <button
            type="submit"
            className={`w-full py-3 rounded-lg font-bold text-white transition ${
              isComplete && !submitting
                ? "bg-blue-600 hover:bg-blue-700"
                : "bg-gray-400 cursor-not-allowed"
            }`}
            disabled={!isComplete || submitting}
          >
            {submitting ? "Listing..." : "List Property"}
          </button>
          {success && <div className="text-green-600 text-center">{success}</div>}
          {error && <div className="text-red-600 text-center">{error}</div>}
        </form>
      </div>
      <Footer />
    </div>
  );
}