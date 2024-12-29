import React, { useState } from "react";
import FormLayout from "../Layout/FormLayout";
import { Link, useNavigate } from "react-router-dom";
import apiClient from "../ultilities/apiConfig";

function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [tcChecked, setTcChecked] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (loading) return;

    if (!email || !password || !confirmPassword) {
      alert("Please fill in all fields");
      return;
    }

    if (password !== confirmPassword) {
      alert("Passwords do not match");
      return;
    }

    if (!tcChecked) {
      alert("Please accept the terms and conditions");
      return;
    }

    setLoading(true);

    // Make API call to register the user

    const data = {
      email,
      password,
    };
    try {
      const res = await apiClient({
        method: "post",
        url: "/api/register/",
        data,
      });

      if (res.status === 200) {
        alert("Account created successfully");
        setTimeout(() => {
          setLoading(false);
          navigate("/login");
        }, 2000);
      }
    } catch (error) {
      console.log(error);
      setLoading(false);
    }
  };

  return (
    <FormLayout formTitle="Create an account">
      <form className="space-y-4 md:space-y-6" onSubmit={handleSubmit}>
        <div>
          <label
            htmlFor="email"
            className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
          >
            Your email
          </label>
          <input
            type="email"
            name="email"
            id="email"
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            placeholder="name@company.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div>
          <label
            htmlFor="password"
            className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
          >
            Password
          </label>
          <input
            type="password"
            name="password"
            id="password"
            placeholder="••••••••"
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <div>
          <label
            htmlFor="confirm-password"
            className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
          >
            Confirm password
          </label>
          <input
            type="confirm-password"
            name="confirm-password"
            id="confirm-password"
            placeholder="••••••••"
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
        </div>
        <div className="flex items-start">
          <div className="flex items-center h-5">
            <input
              id="terms"
              aria-describedby="terms"
              type="checkbox"
              className="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-primary-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-primary-600 dark:ring-offset-gray-800"
              checked={tcChecked}
              onChange={() => setTcChecked(!tcChecked)}
            />
          </div>
          <div className="ml-3 text-sm">
            <label
              htmlFor="terms"
              className="font-light text-gray-500 dark:text-gray-300"
            >
              I accept the{" "}
              <a
                className="font-medium text-primary-600 hover:underline dark:text-primary-500"
                href="#"
              >
                Terms and Conditions
              </a>
            </label>
          </div>
        </div>
        <button
          type="submit"
          className="w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800"
        >
          Create an account
        </button>
        <p className="text-sm font-light text-gray-500 dark:text-gray-400">
          Already have an account?{" "}
          <Link
            to="/login"
            className="font-medium text-primary-600 hover:underline dark:text-primary-500"
          >
            Login here
          </Link>
        </p>
      </form>
    </FormLayout>
  );
}

export default Register;
