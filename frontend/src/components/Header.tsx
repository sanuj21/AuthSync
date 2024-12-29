import React from "react";
import logoD from "/logoD.png";
import { Link, useNavigate } from "react-router-dom";

function Header() {
  const navigate = useNavigate();

  const logoutUser = () => {
    localStorage.clear();
    navigate("/login");
  };

  return (
    <header className="flex shadow-lg py-4 px-4 sm:px-10 bg-white font-[sans-serif] min-h-[70px] tracking-wide relative z-50">
      <div className="flex flex-wrap items-center justify-between gap-4 w-full">
        <Link
          to="/"
          className="lg:absolute max-lg:left-10 lg:top-2/4 lg:left-2/4 lg:-translate-x-1/2 lg:-translate-y-1/2 max-sm:hidden"
        >
          <img src={logoD} alt="logo" className="w-36" />
        </Link>
        <a href="#" className="hidden max-sm:block">
          <img src={logoD} alt="logo" className="w-9" />
        </a>
        <div
          id="collapseMenu"
          className="max-lg:hidden lg:!block max-lg:w-full max-lg:fixed max-lg:before:fixed max-lg:before:bg-black max-lg:before:opacity-50 max-lg:before:inset-0 max-lg:before:z-50"
        >
          <button
            id="toggleClose"
            className="lg:hidden fixed top-2 right-4 z-[100] rounded-full bg-white w-9 h-9 flex items-center justify-center border"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="w-3.5 h-3.5 fill-black"
              viewBox="0 0 320.591 320.591"
            >
              <path
                d="M30.391 318.583a30.37 30.37 0 0 1-21.56-7.288c-11.774-11.844-11.774-30.973 0-42.817L266.643 10.665c12.246-11.459 31.462-10.822 42.921 1.424 10.362 11.074 10.966 28.095 1.414 39.875L51.647 311.295a30.366 30.366 0 0 1-21.256 7.288z"
                data-original="#000000"
              />
              <path
                d="M287.9 318.583a30.37 30.37 0 0 1-21.257-8.806L8.83 51.963C-2.078 39.225-.595 20.055 12.143 9.146c11.369-9.736 28.136-9.736 39.504 0l259.331 257.813c12.243 11.462 12.876 30.679 1.414 42.922-.456.487-.927.958-1.414 1.414a30.368 30.368 0 0 1-23.078 7.288z"
                data-original="#000000"
              />
            </svg>
          </button>
          <ul className="lg:flex lg:gap-x-5 max-lg:space-y-3 max-lg:fixed max-lg:bg-white max-lg:w-1/2 max-lg:min-w-[300px] max-lg:top-0 max-lg:left-0 max-lg:p-6 max-lg:h-full max-lg:shadow-md max-lg:overflow-auto z-50">
            <li className="mb-6 hidden max-lg:block">
              <a href="#">
                <img src="./logoD.png" alt="logo" className="w-36" />
              </a>
            </li>
            <li className="max-lg:border-b max-lg:py-3 px-3">
              <Link
                to="/"
                className="hover:text-primary-600 text-primary-600 block font-semibold text-[15px]"
              >
                Home
              </Link>
            </li>
            <li className="max-lg:border-b max-lg:py-3 px-3">
              <Link
                to="/createApp"
                className="hover:text-primary-600 text-[#333] block font-semibold text-[15px]"
              >
                Create App
              </Link>
            </li>
            <li className="max-lg:border-b max-lg:py-3 px-3">
              <Link
                to="#"
                className="hover:text-primary-600 text-[#333] block font-semibold text-[15px]"
              >
                Plans
              </Link>
            </li>
            <li className="max-lg:border-b max-lg:py-3 px-3">
              <Link
                to="#"
                className="hover:text-primary-600 text-[#333] block font-semibold text-[15px]"
              >
                Features
              </Link>
            </li>
          </ul>
        </div>
        <div className="flex items-center ml-auto space-x-6">
          <button className="font-semibold text-[15px] border-none outline-none">
            {!localStorage.getItem("access") ? (
              <Link to="/login" className="text-primary-600 hover:underline">
                Login
              </Link>
            ) : (
              <span
                className="text-primary-600 hover:underline"
                onClick={logoutUser}
              >
                Logout
              </span>
            )}
          </button>
          <Link
            to="register"
            className="px-4 py-2 text-sm rounded-sm font-bold text-white border-2 border-primary-600 bg-primary-600 transition-all ease-in-out duration-300 hover:bg-transparent hover:text-primary-600"
          >
            Sign up
          </Link>
          <button id="toggleOpen" className="lg:hidden">
            <svg
              className="w-7 h-7"
              fill="#333"
              viewBox="0 0 20 20"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                fillRule="evenodd"
                d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
                clipRule="evenodd"
              />
            </svg>
          </button>
        </div>
      </div>
    </header>
  );
}

export default Header;
