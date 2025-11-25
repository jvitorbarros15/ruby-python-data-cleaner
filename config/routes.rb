Rails.application.routes.draw do
  root "pages#home"
  get "pages/home"

  # DATA ROUTES
  get "/data", to: "data#index"
  get "/data/show", to: "data#show"
  post "/data/run", to: "data#run"     # runs python scripts

  # CLEANING ROUTES
  get  "/cleaning",     to: "cleaning#new",    as: :new_cleaning
  post "/cleaning/run", to: "cleaning#create", as: :run_cleaning

  # Health check
  get "up" => "rails/health#show", as: :rails_health_check
end
