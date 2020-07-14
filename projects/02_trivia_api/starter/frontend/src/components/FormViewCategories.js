import React, { Component } from "react";
import $ from "jquery";

import "../stylesheets/FormView.css";

class FormViewCategories extends Component {
  constructor(props) {
    super();
    this.state = {
      type: "",
      categories: {},
    };
  }

  componentDidMount() {
    $.ajax({
      url: `/categories`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({ categories: result.categories });
        return;
      },
      error: (error) => {
        alert("Unable to load categories. Please try your request again");
        return;
      },
    });
  }

  submitQuestion = (event) => {
    event.preventDefault();
    $.ajax({
      url: "/categories/create",
      type: "POST",
      dataType: "json",
      contentType: "application/json",
      data: JSON.stringify({
        type: this.state.type,
      }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        document.getElementById("add-category-form").reset();
        return;
      },
      error: (error) => {
        alert("Unable to add category. Please try your request again");
        return;
      },
    });
  };

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };

  render() {
    return (
      <div id="add-form">
        <h2>Add a New Trivia Category</h2>
        <form
          className="form-view"
          id="add-category-form"
          onSubmit={this.submitQuestion}
        >
          <label>
            Type
            <input type="text" name="type" onChange={this.handleChange} />
          </label>

          <input type="submit" className="button" value="Submit" />
        </form>
      </div>
    );
  }
}

export default FormViewCategories;
