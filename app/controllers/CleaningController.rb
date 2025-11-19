require "json"

# Controller for handling data cleaning requests
# Assumes a Python script at python/check_publications_cleaning.py

class CleaningController < ApplicationController
def create
  uploaded = params[:file]
  raise "No file uploaded" unless uploaded

  upload_path = Rails.root.join("tmp", "uploads", uploaded.original_filename)
  FileUtils.mkdir_p(upload_path.dirname)
  File.binwrite(upload_path, uploaded.read)

  raw_options = params.fetch(:options, {})

  config = {
    remove_duplicates: raw_options["remove_duplicates"] == "1",
    standardize_month: raw_options["standardize_month"] == "1",
    month_column: raw_options["month_column"].presence || "month",
    drop_columns: raw_options["drop_columns"].to_s.split(",").map(&:strip).reject(&:blank?)
    # more options here later
  }

  config_path = Rails.root.join("tmp", "config.json")
  File.write(config_path, JSON.pretty_generate(config))

  output_csv  = Rails.root.join("tmp", "outputs", "cleaned.csv")
  output_xlsx = Rails.root.join("tmp", "outputs", "cleaned.xlsx")
  FileUtils.mkdir_p(output_csv.dirname)

  # Call Python with positional args, no long flags, to avoid any double dash
  system(
    "python3",
    Rails.root.join("python", "check_publications_cleaning.py").to_s,
    upload_path.to_s,
    output_csv.to_s,
    output_xlsx.to_s,
    config_path.to_s
  )

  # Read head of cleaned CSV to show in browser
  require "csv"
  rows = CSV.read(output_csv, headers: true)
  @headers = rows.headers
  @preview_rows = rows.first(20)

  # render your view
end
end
