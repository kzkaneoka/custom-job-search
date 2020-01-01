import React from "react";
import { render, cleanup } from "@testing-library/react";
import "@testing-library/jest-dom/extend-expect";

import JobsList from "../JobsList";

afterEach(cleanup);

const jobs = [
  {
    company: "ABC",
    title: "Software Engineer",
    location: "San Francisco",
    date: "n/a",
    link: "https://www.indeed.com/abc"
  },
  {
    company: "XXX",
    title: "Backend Engineer",
    location: "San Jose",
    date: "n/a",
    link: "https://www.indeed.com/xxx"
  }
];

it("renders", () => {
  const { asFragment } = render(<JobsList jobs={jobs} />);
  expect(asFragment()).toMatchSnapshot();
});
