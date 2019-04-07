var school_id = db.schools.findOne({'name':"北京邮电大学"})._id;
var school_id = db.schools.findOne({'name':"清华大学"})._id;


// db.users.aggregate([
//     {$sort: {follower_count: -1}},
//     {$limit: 20},
//     {$unwind: '$educations'},
// ])

// db.users.aggregate([
//     {$sort: {follower_count: -1}},
//     {$unwind: '$educations'},
//     {$match: {'educations.id': school_id}},
//     {$limit: 2},
// ])


// db.users.aggregate([
//     {$sort: {follower_count: -1}},
//     {$limit: 20},
//     {$unwind: '$educations'},
//     {$match: {'educations.id': "19580559"}},
// ])
// 

db.users.aggregate([
    {$sort: {follower_count: -1}},
    {$match: {'business': {'id': '19550517'}}},
    {$limit: 20},
]);

// $elemMatch does not work in the Aggreggation

// db.users.aggregate([
//     {$sort: {follower_count: -1}},
//     {$limit: 20},
//     {$match: {'educations': [{'name':"北京邮电大学"}]}},
// ])




db.users.find({}, {'educations':{$elemMatch:{'id':school_id}}})

db.users.aggregate([
    {$sort: {follower_count: -1}},
    {$limit: 100},
])

db.users.aggregate([
    {$sort: {voteup_count: -1}},
    {$limit: 20},
])

db.users.aggregate([
    {$sort: {articles_count: -1}},
    {$limit: 20},
])

db.schools.aggregate([
    {$sort: {num: -1}},
    {$limit: 20},
])

db.locations.aggregate([
    {$sort: {num: -1}},
    {$limit: 20},
])
