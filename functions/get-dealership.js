const express = require("express");

const app = express();
const port = 3000;
const Cloudant = require("@cloudant/cloudant");

// Initialize Cloudant connection
function dbCloudantConnect() {
    return new Promise((resolve, reject) => {
        Cloudant(
            {
                // eslint-disable-line'
                iamApiKey: "0t4gHmiuNEaPBkDjsS39BnnfXXN_SJsq4ikGtRTz9Ma-",
                url: "https://1f8ba730-6274-498e-bdc8-06a9d13ea97d-bluemix.cloudantnosqldb.appdomain.cloud",
                // account: "1f8ba730-6274-498e-bdc8-06a9d13ea97d-bluemix",
            },
            (err, cloudant) => {
                if (err) {
                    console.error(
                        "Connect failure: " + err.message + " for Cloudant DB"
                    );
                    reject(err);
                } else {
                    let db = cloudant.use("dealerships");
                    console.info("Connect success! Connected to DB");
                    resolve(db);
                }
            }
        );
    });
}

let db;

dbCloudantConnect()
    .then((database) => {
        db = database;
    })
    .catch((err) => {
        throw err;
    });

app.use(express.json());

// Define a route to get all dealerships with optional state and ID filters
app.get("/dealerships/get", (req, res) => {
    const { state } = req.query;

    if (state) {
        // Fetch dealerships by state abbreviation
        db.find(
            {
                selector: {
                    st: state,
                },
            },
            (err, result) => {
                if (err) {
                    console.error("Error fetching dealerships by state:", err);
                    return res
                        .status(500)
                        .send("Something went wrong on the server.");
                }

                if (result.docs.length === 0) {
                    return res.status(404).send("The state does not exist.");
                }

                return res.json(result.docs);
            }
        );
    } else {
        // Fetch all dealerships if no state provided
        db.list({ include_docs: true }, (err, result) => {
            if (err) {
                console.error("Error fetching all dealerships:", err);
                return res
                    .status(500)
                    .send("Something went wrong on the server.");
            }

            const dealerships = result.rows.map((row) => row.doc);
            return res.json(dealerships);
        });
    }
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
