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

    const locationsInput = getByLabelText("Locations");
    expect(locationsInput).toHaveAttribute("type", "text");
    expect(locationsInput).not.toHaveValue();

    const buttonInput = getByText("Submit");
    expect(buttonInput).toHaveValue("Submit");
  });

  it("a snapshot properly", () => {
    const { asFragment } = renderWithRouter(<SearchForm {...props} />);
    expect(asFragment()).toMatchSnapshot();
  });
});
