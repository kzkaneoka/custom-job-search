import React from "react";
import { cleanup, fireEvent, wait } from "@testing-library/react";
import "@testing-library/jest-dom/extend-expect";

import SearchForm from "../SearchForm";

afterEach(cleanup);

describe("renders", () => {
  const props = {
    handleSearchFormSubmit: () => {
      return true;
    }
  };

  it("properly", () => {
    const { getByText } = renderWithRouter(<SearchForm {...props} />);
    expect(getByText("Job Search")).toHaveClass("title");
  });

  it("default props", () => {
    const { getByLabelText, getByText } = renderWithRouter(
      <SearchForm {...props} />
    );

    const wordsInput = getByLabelText("Words");
    expect(wordsInput).toHaveAttribute("type", "text");
    expect(wordsInput).not.toHaveValue();

    const locationInput = getByLabelText("Location");
    expect(locationInput).toHaveAttribute("type", "text");
    expect(locationInput).not.toHaveValue();

    const buttonInput = getByText("Search Jobs");
    expect(buttonInput).toHaveValue("Search Jobs");
  });

  it("a snapshot properly", () => {
    const { asFragment } = renderWithRouter(<SearchForm {...props} />);
    expect(asFragment()).toMatchSnapshot();
  });
});
